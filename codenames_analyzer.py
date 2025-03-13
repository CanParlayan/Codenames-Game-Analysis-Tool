from playwright.sync_api import sync_playwright, TimeoutError
import time
import json
import os
import re
import argparse
import pyperclip
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from languages import LANGUAGES

console = Console()


def capture_websocket_data(target_url, username="Player", browser_visible=False, max_wait_time=30):
    """Capture WebSocket data from a Codenames game."""

    os.makedirs("codenames_data", exist_ok=True)

    with open("codenames_data/codenames_messages.json", "w") as f:
        f.write("")

    console.print(Panel(f"[bold blue]CODENAMES ANALYSIS TOOL[/bold blue]", subtitle="v1.0"))
    console.print(f"[yellow]Target URL:[/yellow] {target_url}")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=not browser_visible, devtools=browser_visible)
        context = browser.new_context()
        page = context.new_page()

        codenames_messages = []
        found_codenames_message = False
        game_over = False
        game_data = None

        def handle_websocket(websocket):
            console.print(f"[green]WebSocket connected:[/green] {websocket.url}")
            websocket.on("framereceived", lambda payload: handle_frame(websocket.url, payload))

        def handle_frame(url, payload):
            nonlocal found_codenames_message, game_data, game_over, codenames_messages

            try:

                if isinstance(payload, str) and "42/codenames" in payload:

                    match = re.search(r'42/codenames,(.*)', payload)
                    if not match:
                        return

                    json_str = match.group(1)

                    try:
                        data = json.loads(json_str)

                        if not isinstance(data, list) or len(data) < 3:
                            return

                        if "G" not in data[2]:
                            return

                        game_data = data[2]["G"]

                        if game_data.get("matchID") is None:
                            return

                        message_data = {
                            "url": url,
                            "data": payload,
                            "timestamp": time.time()
                        }
                        codenames_messages.append(message_data)

                        if game_data.get("gameOver", False):
                            game_over = True
                            console.print("[bold red]Game over![/bold red]")

                        with open("codenames_data/codenames_messages.json", "a") as f:
                            json.dump(message_data, f)
                            f.write("\n")
                        found_codenames_message = True

                    except json.JSONDecodeError:
                        pass

            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {str(e)}")

        page.on("websocket", handle_websocket)

        try:
            page.goto(target_url, timeout=30000)
            console.print("[bold green]✓ Page loaded successfully![/bold green]")
        except TimeoutError:
            console.print("[bold red]⚠ Warning: Page could not be loaded!")
            return [], None, False

        try:
            page.fill('#nickname-input', username)
            page.click('button[role="button"][type="submit"]')
            console.print("[bold green]Username entered and joined room...[/bold green]")

            page.wait_for_selector('div#gamescene', timeout=30000)
            console.print("[bold green]✓ Game scene loaded successfully![/bold green]")
        except TimeoutError:
            console.print("[bold red]⚠ Warning: Game scene not found!")
            return [], None, False
        except Exception as e:
            console.print(f"[bold red]⚠ Error: {str(e)}")
            return [], None, False

        console.print(
            "[bold red]⚠ After the game scene is loaded, check if a player has entered a team or has been switched a "
            "team. If not, switch your team or join a team. \n[bold yellow]Confirm if this has been done. (Y/N): ")
        setup_ready = input().strip().lower() == 'y'

        if not setup_ready:
            console.print("[bold yellow]Setup not ready, please complete the setup and try again.[/bold yellow]")
            return [], None, False

        start_time = time.time()
        while (time.time() - start_time) < max_wait_time:
            if found_codenames_message:
                console.print(f"[bold green]Receiving data... ({len(codenames_messages)} messages)")
            else:
                remaining = max_wait_time - (time.time() - start_time)
                console.print(f"[bold yellow]Waiting for data... ({remaining:.0f} seconds remaining)")
            time.sleep(2)

        browser.close()

        if not found_codenames_message:
            console.print("[bold red]⚠ Warning: No WebSocket messages containing '42/codenames' received!")
            console.print("[yellow]Possible reasons:[/yellow]")
            console.print("1. The game may not have started yet")
            console.print("2. WebSocket connection could not be established")
            console.print("3. Insufficient wait time (can be increased with the --wait parameter)")
            console.print(
                "4. After the game scene is loaded, check if a player has entered a team or has been switched a team. "
                "If not, switch your team or join a team. Confirm if this has been done.")
        else:
            console.print(
                f"[bold green]✓ Data collection completed! {len(codenames_messages)} codenames messages received.")

        return codenames_messages, game_data, game_over


def evaluate_card_colors(codenames_messages_file=None, messages=None):
    """Evaluate card colors from Codenames messages"""

    result = {
        "red_cards": [],
        "blue_cards": [],
        "black_card": None,
        "gray_cards": [],
        "all_cards": {},
        "turn": None,
        "red_remaining": 0,
        "blue_remaining": 0,
        "game_over": False
    }

    try:

        if codenames_messages_file and not messages:

            if not os.path.exists(codenames_messages_file):
                console.print(f"[bold red]Error: File {codenames_messages_file} not found.[/bold red]")
                return None

            if os.path.getsize(codenames_messages_file) == 0:
                console.print(f"[bold red]Error: File {codenames_messages_file} is empty.[/bold red]")
                return None

            with open(codenames_messages_file, "r") as f:
                file_content = f.read().strip()
                if not file_content:
                    console.print(f"[bold red]Error: File {codenames_messages_file} contains no data.[/bold red]")
                    return None

                f.seek(0)
                messages = []
                for line in f:
                    line = line.strip()
                    if line:
                        try:

                            message_obj = json.loads(line)
                            messages.append(message_obj)
                        except json.JSONDecodeError:
                            console.print(
                                f"[bold yellow]Warning: Skipping invalid JSON line: {line[:50]}...[/bold yellow]")

                if not messages:
                    console.print(f"[bold red]Error: No valid messages found in {codenames_messages_file}.[/bold red]")
                    return None

        elif not messages:
            console.print("[bold red]Error: No message data found![/bold red]")
            return None

    except Exception as e:
        console.print(f"[bold red]Error reading file: {str(e)}[/bold red]")
        return None

    card_data_found = False
    for message in messages:
        data = message.get("data", "")
        if not isinstance(data, str) or "42/codenames" not in data:
            continue

        match = re.search(r'42/codenames,(.*)', data)
        if not match:
            continue

        json_str = match.group(1)

        try:
            data = json.loads(json_str)

            if not isinstance(data, list) or len(data) < 3:
                continue

            if "G" not in data[2]:
                continue

            game_data = data[2]["G"]
            card_data_found = True

            if game_data.get("gameOver", False):
                result["game_over"] = True

            result["turn"] = game_data.get("currentTeam", game_data.get("turn", "unknown"))

            result["red_remaining"] = game_data.get("score", {}).get("red", 0)
            result["blue_remaining"] = game_data.get("score", {}).get("blue", 0)

            anim_tokens = game_data.get("animTokens", [])

            word_cards = {}
            for token in anim_tokens:
                if token.get("type") == "wordCard":
                    location = token.get("location", {})
                    if location.get("name") == "board":
                        x = location.get("x", 0)
                        y = location.get("y", 0)
                        position = y * 5 + x
                        word = token.get("data", {}).get("word", "")
                        word_cards[position] = {
                            "word": word,
                            "revealed": token.get("data", {}).get("revealed", False),
                            "color": "unknown"
                        }

            for token in anim_tokens:
                if token.get("type") == "coverCard":
                    token_id = token.get("id", "")
                    parts = token_id.split("/")
                    if len(parts) >= 3 and parts[0] == "coverCard":
                        color = parts[1]
                        position_str = parts[2]

                        if position_str.isdigit():
                            position = int(position_str)

                            if position in word_cards:
                                word_cards[position]["color"] = color

            for position, card_info in word_cards.items():
                word = card_info["word"]
                color = card_info["color"]
                revealed = card_info["revealed"]

                if color == "red" and word not in result["red_cards"]:
                    result["red_cards"].append(word)
                elif color == "blue" and word not in result["blue_cards"]:
                    result["blue_cards"].append(word)
                elif color == "black" and not result["black_card"]:
                    result["black_card"] = word
                elif color == "gray" and word not in result["gray_cards"]:
                    result["gray_cards"].append(word)

                result["all_cards"][word] = {
                    "position": position,
                    "color": color,
                    "revealed": revealed,
                }

        except Exception as e:
            console.print(f"[bold red]Message processing error: {str(e)}[/bold red]")
            continue

    if not card_data_found:
        console.print("[bold yellow]No card data found in any message![/bold yellow]")

    return result


def print_card_colors(card_data):
    """Display card colors in a readable format"""
    if not card_data:
        console.print("[bold red]No card data to display![/bold red]")
        return

    console.print(Panel("[bold]CODENAMES GAME STATUS[/bold]", style="blue"))

    console.print(f"[bold]Turn:[/bold] {'RED' if card_data.get('turn') == 'red' else 'BLUE'} Team")
    console.print(
        f"[bold]Remaining Cards:[/bold] Red: {card_data.get('red_remaining', 0)}, Blue: "
        f"{card_data.get('blue_remaining', 0)}")

    red_table = Table(title="RED CARDS", style="red")
    red_table.add_column("Word", style="red")
    red_table.add_column("Revealed?", style="red")
    for word in card_data.get("red_cards", []):
        revealed = "✓" if card_data["all_cards"][word]["revealed"] else "✗"
        red_table.add_row(word, revealed)
    console.print(red_table)

    blue_table = Table(title="BLUE CARDS", style="blue")
    blue_table.add_column("Word", style="blue")
    blue_table.add_column("Revealed?", style="blue")
    for word in card_data.get("blue_cards", []):
        revealed = "✓" if card_data["all_cards"][word]["revealed"] else "✗"
        blue_table.add_row(word, revealed)
    console.print(blue_table)

    if card_data.get("black_card"):
        black_word = card_data.get("black_card")
        revealed = card_data["all_cards"][black_word]["revealed"]
        console.print(Panel(f"[bold]ASSASSIN CARD:[/bold] {black_word} {'(Revealed)' if revealed else '(Hidden)'}",
                            style="red on black"))

    neutral_table = Table(title="NEUTRAL CARDS", style="white")
    neutral_table.add_column("Word", style="white")
    neutral_table.add_column("Revealed?", style="white")
    for word in card_data.get("gray_cards", []):
        revealed = "✓" if card_data["all_cards"][word]["revealed"] else "✗"
        neutral_table.add_row(word, revealed)
    console.print(neutral_table)


def generate_ai_prompt(card_data, team, language="tr"):
    """Generate a prompt for the AI service based on the card data, selected team, and language."""
    if not card_data:
        console.print("[bold red]No card data to generate prompt from![/bold red]")
        return None

    unrevealed_red = [word for word in card_data.get("red_cards", [])
                      if not card_data["all_cards"][word]["revealed"]]
    unrevealed_blue = [word for word in card_data.get("blue_cards", [])
                       if not card_data["all_cards"][word]["revealed"]]
    assassin_card = card_data.get("black_card")
    if assassin_card and card_data["all_cards"][assassin_card]["revealed"]:
        assassin_card = None

    current_team = 'RED' if team == 'red' else 'BLUE'
    other_team = 'BLUE' if current_team == 'RED' else 'RED'
    if language not in LANGUAGES:
        console.print(f"[bold red]Unsupported language: {language}[/bold red]")
        return None

    template = LANGUAGES[language]["prompt_template"].strip()
    prompt = template.format(
        current_team=current_team,
        other_team=other_team,
        unrevealed_red=", ".join(unrevealed_red),
        unrevealed_blue=", ".join(unrevealed_blue),
        assassin_card=assassin_card
    )

    return prompt


def display_manual_instructions():
    """Display instructions for the manual method"""
    console.print("""
1. [bold]Open any free AI service[/bold] in your browser (like ChatGPT, Claude, Bard, etc.)
2. [bold]Paste the prompt[/bold] into the AI service's input box.
3. [bold]Send the prompt[/bold] and get your clue suggestions.
4. [bold]Choose the best clue[/bold] for your team's strategy!

[bold yellow]Note:[/bold yellow] The prompt has been formatted specifically for the Codenames game with the current game
 state.
    """)


def main():
    parser = argparse.ArgumentParser(description='Codenames Game Analysis Tool')
    parser.add_argument('--url', type=str, help='Codenames room URL')
    parser.add_argument('--username', type=str, default='Spectator', help='Username')
    parser.add_argument('--browser', action='store_true', help='Run browser in visible mode')
    parser.add_argument('--wait', type=int, default=10, help='Maximum wait time (seconds)')
    parser.add_argument('--manual', action='store_true', default=True, help='Use manual mode for AI prompt')
    args = parser.parse_args()

    target_url = args.url
    if not target_url:
        target_url = input("Enter Codenames room URL: ")

    team = input("Which team are you on? (red/blue): ").strip().lower()
    while team not in ["red", "blue"]:
        console.print("[bold red]Invalid team! Please enter 'red' or 'blue'.[/bold red]")
        team = input("Which team are you on? (red/blue): ").strip().lower()

    console.print(Panel("[bold]AVAILABLE LANGUAGES[/bold]", style="blue"))
    for code, lang_info in LANGUAGES.items():
        console.print(f"{code}. {lang_info['description']}")

    language_choice = input("Select a language (e.g., 'tr' for Turkish, 'en' for English): ").strip().lower()

    if not language_choice:
        language_choice = "tr"

    if language_choice not in LANGUAGES:
        console.print(f"[bold red]Unsupported language: {language_choice}[/bold red]")
        return

    codenames_messages, game_data, _ = capture_websocket_data(
        target_url,
        username=args.username,
        browser_visible=args.browser,
        max_wait_time=args.wait
    )

    if not codenames_messages:
        console.print("[bold red]⚠ Analysis not possible: No WebSocket messages received.[/bold red]")
        return

    card_data = evaluate_card_colors("codenames_data/codenames_messages.json")
    if card_data:
        print_card_colors(card_data)

        ai_prompt = generate_ai_prompt(card_data, team, language_choice)

        if ai_prompt:

            with open("codenames_data/ai_prompt.txt", "w", encoding="utf-8") as f:
                f.write(ai_prompt)

            console.print(f"[bold green]Prompt generated and saved to codenames_data/ai_prompt.txt[/bold green]")

            try:
                pyperclip.copy(ai_prompt)
                console.print("[bold green]✓ Prompt copied to clipboard![/bold green]")
            except Exception as e:
                console.print(f"[bold yellow]Could not copy to clipboard: {str(e)}[/bold yellow]")
                console.print("[yellow]Please manually copy the prompt from the file.[/yellow]")

            display_manual_instructions()
    else:
        console.print("[bold red]⚠ Analysis not possible: Could not retrieve card data.[/bold red]")

    console.print("[bold green]Analysis completed. Exiting...[/bold green]")


if __name__ == "__main__":
    main()

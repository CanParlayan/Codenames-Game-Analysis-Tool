# Codenames Analysis Tool

A powerful utility for analyzing Codenames game state and generating AI-assisted clue suggestions for spymasters.

## Overview

The Codenames Analysis Tool connects to an active Codenames game, captures the game state through WebSocket monitoring, and helps spymasters generate effective clues by preparing prompts for AI assistants like ChatGPT, Claude, or Bard.

![Codenames Analysis Tool](https://github.com/CanParlayan/Codenames-Game-Analysis-Tool/blob/main/img.png)

## Features

- **Live Game Analysis**: Connects to active Codenames games to extract the current board state
- **Team Intelligence**: Identifies all cards and their colors (red, blue, neutral, assassin)
- **Revealed Card Tracking**: Monitors which cards have already been revealed
- **AI Prompt Generation**: Creates optimized prompts for AI assistants in multiple languages
- **Multi-language Support**: Generates prompts in different languages for international play
- **User-friendly Interface**: Beautiful console interface with color-coded information

## Requirements

- Python 3.7+
- Playwright
- Rich (for console formatting)
- pyperclip (for clipboard functionality)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/username/codenames-analysis-tool.git
   cd codenames-analysis-tool
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

Run the tool with:

```
python codenames_analyzer.py
```

Or with optional arguments:

```
python codenames_analyzer.py --url "https://codenames.game/room/your-room-code" --username "YourName" --browser --wait 15
```

### Command Line Options

- `--url`: The URL of the Codenames room (can also be entered when prompted)
- `--username`: Your display name in the game (default: "Spectator")
- `--browser`: Run the browser in visible mode (default: headless)
- `--wait`: Maximum wait time in seconds for collecting data (default: 10)
- `--manual`: Use manual mode for AI prompt (default: True)

### Workflow

1. Enter the Codenames room URL when prompted
2. Select your team (red or blue)
3. Choose your preferred language for AI prompts
4. Wait while the tool captures game data
5. Review the analyzed game state displayed in the console
6. Use the generated AI prompt (automatically copied to clipboard) with your preferred AI service
7. Get clue suggestions from the AI and make your strategic decision

## Languages Supported

- English (en)
- Turkish (tr)
- Italian (it)
- And more in the future...

## Future Plans

- API integration for AI services

## How It Works

The tool uses Playwright to open a browser connection to the Codenames game, intercepts WebSocket traffic to extract game state information, analyzes the data to determine card colors and game status, and then formats this information into an optimized prompt for AI assistants.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is intended for practice, learning, and casual play. Please use responsibly and respect the terms of service of both Codenames and any AI services you use.

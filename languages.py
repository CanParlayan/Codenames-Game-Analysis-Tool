LANGUAGES = {
    "tr": {
        "description": "Türkçe",
        "prompt_template": '''Codenames - {current_team} Takımı İçin En İyi İpucu

Ben {current_team} takımındayım ve takım arkadaşlarıma tek kelimelik bir Türkçe ipucu vermem gerekiyor. İpucum, sadece {current_team} kartlarını çağrıştırmalı, {other_team} kartlarına veya casus karta {assassin_card} kesinlikle yönlendirmemeli.

Açılmamış kartlar:

RED kartlar: {unrevealed_red}
BLUE kartlar: {unrevealed_blue}
BLACK kart: {assassin_card}

İdeal İpucunu Bulmak İçin Adımlar
{current_team} kartlar arasında ortak bir tema, kavram veya ilişki bul.

Bu tema, sadece {current_team} kartlarını birleştirmeli, {other_team} kartlarını veya {assassin_card} kartla bağlantı 
kurmamalı. Gerekirse {current_team} kartları 2'li veya 3'lü gruplar halinde ele alabilirsin. Bulduğun temayı tek 
kelimelik bir ipucu olarak öner.

İpucu Türkçede doğal, anlaşılır ve günlük kullanıma uygun olmalı.
Gerekirse günlük dilde kullanılan popüler kelimeleri veya memeleri değerlendirebilirsin.
İpucunun neden {current_team} kartlarını çağrıştırdığını açıkla.

Karşı takımın ({other_team}) kartlarıyla veya {assassin_card} ile neden bağlantı kurmadığını doğrula. Hedef: {current_team} takımının en fazla kartı açmasını sağlamak, {other_team} kartlarını veya {assassin_card} çağrıştırmaktan kaçınmak.'''
    },
    "en": {
        "description": "English",
        "prompt_template": '''Codenames - Best Hint for {current_team} Team

I am on the {current_team} team and need to give my teammates a single-word hint in English. The hint should only evoke {current_team} cards and must not lead to {other_team} cards or the assassin card {assassin_card}.

Unrevealed Cards:

RED cards: {unrevealed_red}

BLUE cards: {unrevealed_blue}

BLACK card: {assassin_card}

Steps to Find the Ideal Hint:

Look for a common theme, concept, or connection among the {current_team} cards.

This theme should only connect the {current_team} cards and must not relate to {other_team} cards or the {assassin_card}.

If necessary, group {current_team} cards into pairs or triplets to find a connection.

Suggest the theme as a single-word hint in English.

The hint should be natural, understandable, and suitable for everyday use in English.

You can also consider popular words or memes used in daily language.

Explain why the hint evokes {current_team} cards.

Confirm why the hint does not connect to {other_team} cards or the {assassin_card}.

Goal: Help the {current_team} team reveal as many cards as possible while avoiding {other_team} cards or the {assassin_card}.'''
    },
    "it": {
        "description": "Italiano",
        "prompt_template": '''Codenames - Il Miglior Indizio per la Squadra {current_team}

Sono nella squadra {current_team} e devo dare ai miei compagni un indizio di una sola parola in italiano. L'indizio deve evocare solo le carte {current_team} e non deve portare alle carte {other_team} o alla carta assassina {assassin_card}.

Carte non Rivelate:

Carte ROSSE: {unrevealed_red}

Carte BLU: {unrevealed_blue}

Carta NERA: {assassin_card}

Passaggi per Trovare l'Indizio Ideale:

Cerca un tema, concetto o connessione comune tra le carte {current_team}.

Questo tema deve collegare solo le carte {current_team} e non deve relazionarsi alle carte {other_team} o alla carta {assassin_card}.

Se necessario, raggruppa le carte {current_team} in coppie o triplette per trovare una connessione.

Suggerisci il tema come un indizio di una sola parola in italiano.

L'indizio deve essere naturale, comprensibile e adatto all'uso quotidiano in italiano.

Puoi anche considerare parole popolari o meme usati nel linguaggio quotidiano.

Spiega perché l'indizio evoca le carte {current_team}.

Conferma perché l'indizio non si collega alle carte {other_team} o alla carta {assassin_card}.

Obiettivo: Aiutare la squadra {current_team} a rivelare quante più carte possibili, evitando le carte {other_team} o la carta {assassin_card}.'''
    }
}
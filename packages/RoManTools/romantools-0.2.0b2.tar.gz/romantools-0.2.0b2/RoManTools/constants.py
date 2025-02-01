"""
Constants for romanized Mandarin text processing.

This module provides various constants used throughout the text processing system, including:
- Vowels set for identifying vowel characters.
- Apostrophes set for identifying apostrophe characters.
- Dashes set for identifying dash characters.
- Supported contractions set for identifying valid contractions.

Constants:
    vowels (Set[str]): A set of vowel characters used in romanized Mandarin text.
    apostrophes (Set[str]): A set of apostrophe characters used in romanized Mandarin text.
    dashes (Set[str]): A set of dash characters used in romanized Mandarin text.
    supported_contractions (Set[str]): A set of valid contractions used in romanized Mandarin text.
"""

vowels = {'a', 'e', 'i', 'o', 'u', 'ü', 'v', 'ê', 'ŭ'}
apostrophes = {"'", "’", "‘", "ʼ", "ʻ", "`"}
dashes = {"-", "–", "—"}
supported_contractions = {"s", "d", "ll"}
supported_methods = {
    'pinyin': {'shorthand': 'py', 'pretty': 'Pinyin'},
    'wade-giles': {'shorthand': 'wg', 'pretty': 'Wade-Giles'}
}
shorthand_to_full = {v['shorthand']: k for k, v in supported_methods.items()}
full_to_shorthand = {k: v['shorthand'] for k, v in supported_methods.items()}

import json
import os
from game_data import Character, classes  # adjust import if needed

SAVE_DIR = "characters"

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

def save_character(character):
    data = {
        "name": character.name,
        "class": character.char_class,
        "max_hp": character.max_hp,
        "hp": character.hp,
        "xp": getattr(character, "xp", 0),
        "traits": getattr(character, "traits", []),
        "wins": getattr(character, "wins", 0),
        "losses": getattr(character, "losses", 0),
        "level": getattr(character, "level", 1)  # Default level to 1 if not present
    }
    with open(f"{SAVE_DIR}/{character.name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_character(name):
    filepath = f"{SAVE_DIR}/{name}.json"
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    char_class = data["class"]
    char = Character(name, char_class)
    char.max_hp = data.get("max_hp", classes[char_class]["hp"])
    char.hp = data.get("hp", classes[char_class]["hp"])
    char.xp = data.get("xp", 0)
    char.traits = data.get("traits", [])
    char.wins = data.get("wins", 0)
    char.losses = data.get("losses", 0)
    char.level = data.get("level", 1)  # Default level to 1 if not present
    return char


def list_saved_characters():
    files = os.listdir(SAVE_DIR)
    return [f[:-5] for f in files if f.endswith(".json")]

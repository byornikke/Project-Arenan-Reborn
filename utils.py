import json

# === Monster Data ===
def load_monsters(filename="data/monsters.json"):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

import random

# === Character Classes ===
classes = {
    "Warrior": {"hp": 100, "damage": [8, 16], "reaction": [4, 8], "level": 1},
    "Ranger":  {"hp": 80,  "damage": [10, 20], "reaction": [6, 12], "level": 1},
    "Mage":    {"hp": 60,  "damage": [5, 25], "reaction": [5, 10], "level": 1},
    "Rogue":   {"hp": 70,  "damage": [7, 18], "reaction": [7, 14], "level": 1},
    "Paladin": {"hp": 120, "damage": [6, 15], "reaction": [3, 6], "level": 1},
    "Bard":    {"hp": 75,  "damage": [4, 12], "reaction": [6, 10], "level": 1},
    "Cleric":  {"hp": 90,  "damage": [3, 10], "reaction": [5, 8], "level": 1},
    "Druid":   {"hp": 85,  "damage": [4, 14], "reaction": [4, 9], "level": 1},
    "Shaman":  {"hp": 95,  "damage": [5, 17], "reaction": [4, 10], "level": 1},
}

# === Character Class ===
class Character:
    def __init__(self, name, char_class, hp=None, damage=None, reaction=None, level=None):
        self.name = name
        self.char_class = char_class
        self.hp = hp if hp is not None else classes[char_class]["hp"]
        self.max_hp = self.hp
        self.damage = damage if damage else classes[char_class]["damage"]
        self.reaction = reaction if reaction else classes[char_class]["reaction"]
        self.xp = 0
        self.traits = []
        self.wins = 0
        self.losses = 0
        self.level = level if level is not None else classes[char_class]["level"]

    def __str__(self):
        return f"{self.name} the {self.char_class}."

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        if random.random() > 0.8:  # 20% chance to miss
            damage = 0
            return damage
        damage = random.randint(*self.damage)
        target.hp -= damage
        if target.hp <= 0:
            target.hp = 0
            target.is_alive = lambda: False  # Mark as dead
        return damage
    
    def initiative(self):
        return random.uniform(*self.reaction)

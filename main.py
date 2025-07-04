# Text-Based Arena MVP (Terminal Version)
import random
import json
from character_manager import save_character, load_character, list_saved_characters
from game_data import classes, Character  # Ensure this imports your character classes
from battle import battle, generate_attack_text, generate_death_text, heal_character, post_game_rewards
from utils import load_monsters  # Ensure this imports your monster loading function

def get_monster():
    monsters = load_monsters()
    name = random.choice(list(monsters.keys()))
    data = monsters[name]
    return Character(name, data["class"], hp=data["hp"], damage=data["damage"], reaction=data["reaction"], level=data.get("level", 1))

# === Environments ===
def call_for_env():
    environments = [
    "A bustling marketplace",
    "A dark alleyway",
    "A rocky mountain pass",
    "A foggy moor",
    "A sunlit meadow",
    "A shadowy cave",
    "A frozen tundra"
]
    return random.choice(environments)

# === Opponent Selection ===
def choose_opponent():
    if input("Do you want to fight a monster? (yes/no): ").lower() == "yes":
        monster = get_monster()
        print("\n You come face to face with " + str(monster))  # Print monster details
        return monster
    else:
        print("For opponent, available saved characters:")
        return load_or_create_character()
        
# === Character Management ===
def load_or_create_character():
    print("\nSaved characters:", ", ".join(list_saved_characters()) or "None")
    use_saved = input("Do you want to load a saved character? (yes/no): ").lower()

    if use_saved == "yes":
        name = input("Enter character name: ")
        char = load_character(name)
        if char:
            print(f"Loaded character '{name}' ({char.char_class}) with {char.hp} HP.")
            return char
        else:
            print("Character not found. You'll need to create a new one.")

    name = input("Enter name for your new fighter: ")
    char_class = input("Choose class (Warrior/Ranger/Mage/Rogue/Paladin): ").capitalize()
    while char_class not in classes:
        print("Invalid class.")
        char_class = input("Choose class (Warrior/Ranger/Mage/Rogue/Paladin): ").capitalize()

    return Character(name, char_class, hp=classes[char_class]["hp"], max_hp=classes[char_class]["hp"], reaction=classes[char_class]["reaction"], damage=classes[char_class]["damage"])

# === Main ===
def main():
    print("Welcome to Arenan Reborn!\n")
    player = load_or_create_character()
    opponent = choose_opponent()
    # Check for same character
    while opponent.name == player.name:
        print("You cannot fight yourself! Please choose a different opponent.")
        opponent = choose_opponent()
    env = call_for_env()

    winner, loser = battle(player, opponent, env)
    post_game_rewards(winner, loser)
    heal_character(player)
    save_character(player)
    # Save opponent only if it's not a monster
    monsters = load_monsters()
    if opponent.name not in monsters:
        heal_character(opponent)
        save_character(opponent)

while True:
    main()
    play_again = input("Do you want to play again? (yes/no): ")
    if play_again.lower() != "yes":
        print("Thanks for playing!")
        break
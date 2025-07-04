# Text-Based Arena MVP (Terminal Version)
import random
import json
from character_manager import save_character, load_character, list_saved_characters
from game_data import classes, Character  # Ensure this imports your character classes



# === Monster Data ===
def load_monsters(filename="monsters.json"):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)

def get_monster():
    monsters = load_monsters()
    name = random.choice(list(monsters.keys()))
    data = monsters[name]
    return Character(name, data["class"], hp=data["hp"], damage=data["damage"], reaction=data["reaction"])


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

def choose_opponent():
    if input("Do you want to fight a monster? (yes/no): ").lower() == "yes":
        monster = get_monster()
        print("\n You come face to face with " + str(monster))  # Print monster details
        return monster
    else:
        print("For opponent, available saved characters:")
        return load_or_create_character()
        

# === Experience System ===
def post_game_rewards(winner, loser):
    if winner is None:
        return  # Monster won, no XP for player
    xp_gained = 50  # Base XP for winning
    winner.xp += xp_gained
    winner.wins += 1
    loser.losses += 1
    print(f"{winner.name} gained {xp_gained} XP!")

# === Healing System ===
def heal_character(character):
    character.hp = character.max_hp

# === Battle Text Samples ===
def generate_attack_text(attacker, defender, damage, environment):
    hurt = ""
    if damage == 0:
        return random.choice(hit_lines["miss"]).format(attacker=attacker.name, defender=defender.name, environment=environment)
    if damage < defender.hp / 4:
        return ( random.choice(hit_lines["weak"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                 random.choice(hurt_lines["weak"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp / 2:
        return ( random.choice(hit_lines["mediocre"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                 random.choice(hurt_lines["mediocre"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp / 1.2: # change to 1 + give up threshold
        return ( random.choice(hit_lines["strong"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                random.choice(hurt_lines["strong"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp:
        return ( random.choice(hit_lines["deadly"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                random.choice(hurt_lines["deadly"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    else:
        defender.hp = 0  # Ensure defender is dead
        return generate_death_text(attacker, defender)

def generate_death_text(attacker, defender):
    return random.choice(hit_lines["death"]).format(attacker=attacker.name, defender=defender.name)

def parse_hit_lines(filename):
    categories = {"weak": [], "mediocre": [], "strong": [], "deadly": [], "miss": [], "death": []}
    current = None
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                key = line[1:-1]
                if key in categories:
                    current = key
            elif line and current:
                categories[current].append(line)
    return categories

# Load hit lines at the top of your file
hit_lines = parse_hit_lines("hit_lines.txt")

def parse_hurt_lines(filename):
    categories = {"weak": [], "mediocre": [], "strong": [], "deadly": []}
    current = None
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                key = line[1:-1]
                key = line[1:-1]
                if key in categories:
                    current = key
            elif line and current:
                categories[current].append(line)
    return categories

# Load hurt lines at the top of your file
hurt_lines = parse_hurt_lines("hurt_lines.txt")


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

# === Game Loop ===
def battle(player, monster, env):
    print("\n--- BATTLE BEGINS ---")
    print(f"Environment: {env}")

    player_reaction = player.initiative()
    monster_reaction = monster.initiative()
    if player_reaction < monster_reaction:
        attacker, defender = monster, player
    else:
        attacker, defender = player, monster

    round_num = 1
    while player.is_alive() and monster.is_alive():
        print(f"-- Round {round_num} --")

        # First attack
        dmg = attacker.attack(defender)
        print(generate_attack_text(attacker, defender, dmg, env))
        if not defender.is_alive():
            print(f"\n{attacker.name} is victorious!")
            break

        # Swap roles
        attacker, defender = defender, attacker

        # Second attack
        dmg = attacker.attack(defender)
        print(generate_attack_text(attacker, defender, dmg, env))
        if not defender.is_alive():
            print(f"\n{attacker.name} is victorious!")
            break

        # Optionally swap back based on initiative
        attack_react = attacker.initiative()
        defend_react = defender.initiative()
        if attack_react < defend_react:
            attacker, defender = defender, attacker

        round_num += 1
        input("\nPress Enter to start the next round...\n")
    # Return the winner only if it's not a monster
    monsters = load_monsters()
    if attacker.name not in monsters:
        return attacker, defender
    else:
        return None, attacker  # Monster won, player lost

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
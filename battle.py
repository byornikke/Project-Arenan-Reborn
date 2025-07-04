import random
from character_manager import Character  # Ensure this imports your character class
from utils import load_monsters  # Ensure this imports your monster loading function

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

def parse_hurt_lines(filename):
    categories = {"weak": [], "mediocre": [], "strong": [], "deadly": []}
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

hit_lines = parse_hit_lines("text/hit_lines.txt")
hurt_lines = parse_hurt_lines("text/hurt_lines.txt")

def generate_attack_text(attacker, defender, damage, environment):
    if damage == 0:
        return random.choice(hit_lines["miss"]).format(attacker=attacker.name, defender=defender.name, environment=environment)
    if damage < defender.hp / 4:
        return ( random.choice(hit_lines["weak"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                 random.choice(hurt_lines["weak"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp / 2:
        return ( random.choice(hit_lines["mediocre"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                 random.choice(hurt_lines["mediocre"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp / 1.2:
        return ( random.choice(hit_lines["strong"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                random.choice(hurt_lines["strong"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    elif damage < defender.hp:
        return ( random.choice(hit_lines["deadly"]).format(attacker=attacker.name, defender=defender.name, environment=environment) + " " +
                random.choice(hurt_lines["deadly"]).format(attacker=attacker.name, defender=defender.name) + f" ({damage})")
    else:
        defender.hp = 0
        return generate_death_text(attacker, defender)

def generate_death_text(attacker, defender):
    return random.choice(hit_lines["death"]).format(attacker=attacker.name, defender=defender.name)

def post_game_rewards(winner, loser):
    if winner is None:
        return  # Monster won, no XP for player
    xp_gained = 50  # Base XP for winning
    winner.xp += xp_gained
    print(f"{winner.name} gained {xp_gained} XP!")
    if winner.xp >= winner.level * 100:  # Level up condition
        winner.level += 1
        winner.xp = 0
        print(f"{winner.name} leveled up to level {winner.level}!")
    winner.wins += 1
    loser.losses += 1

def heal_character(character):
    character.hp = character.max_hp


def battle(player, opponent, env):
    print("\n--- BATTLE BEGINS ---")
    print(f"Environment: {env}")
    print(f"\n{player.name} the {player.char_class} (Level {player.level}) are fighting {opponent.name} the {opponent.char_class} (Level {opponent.level})!")
    player_reaction = player.initiative()
    opponent_reaction = opponent.initiative()
    if player_reaction < opponent_reaction:
        attacker, defender = opponent, player
    else:
        attacker, defender = player, opponent

    round_num = 1
    while player.is_alive() and opponent.is_alive():
        print(f"-- Round {round_num} --")

        dmg = attacker.attack(defender)
        print(generate_attack_text(attacker, defender, dmg, env))
        if not defender.is_alive():
            print(f"\n{attacker.name} is victorious!")
            break

        attacker, defender = defender, attacker

        dmg = attacker.attack(defender)
        print(generate_attack_text(attacker, defender, dmg, env))
        if not defender.is_alive():
            print(f"\n{attacker.name} is victorious!")
            break

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
        return None, attacker
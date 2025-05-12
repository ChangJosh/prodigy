import random
import time

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 50
        self.max_hp = 50
        self.exp = 0
        self.exp_to_level = 100
        self.spells = {
            "Fireball": {"damage": 10, "difficulty": "easy"},
            "Ice Shard": {"damage": 15, "difficulty": "medium"},
            "Lightning Bolt": {"damage": 20, "difficulty": "hard"}
        }
    
    def level_up(self):
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.exp -= self.exp_to_level
        self.exp_to_level = int(self.exp_to_level * 1.5)
        print(f"\n🌟 {self.name} leveled up to Level {self.level}! 🌟")
        print(f"Max HP increased to {self.max_hp}!")
    
    def heal(self, amount):
        self.hp = min(self.hp + amount, self.max_hp)
        print(f"\nYou healed for {amount} HP! Current HP: {self.hp}/{self.max_hp}")
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"\n💀 {self.name} has been defeated! 💀")
            return True
        print(f"\nYou took {damage} damage! HP: {self.hp}/{self.max_hp}")
        return False
    
    def gain_exp(self, amount):
        self.exp += amount
        print(f"\nYou gained {amount} EXP!")
        if self.exp >= self.exp_to_level:
            self.level_up()
    
    def display_stats(self):
        print(f"\n=== {self.name} ===")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"EXP: {self.exp}/{self.exp_to_level}")
        print("Spells:")
        for spell, details in self.spells.items():
            print(f"- {spell}: {details['damage']} damage ({details['difficulty']} math)")

class Monster:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.hp = 30 + (level * 10)
        self.max_hp = self.hp
        self.damage = 5 + (level * 2)
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print(f"\n💀 {self.name} has been defeated! 💀")
            return True
        print(f"\n{self.name} took {damage} damage! HP: {self.hp}/{self.max_hp}")
        return False
    
    def attack(self, player):
        print(f"\n{self.name} attacks you!")
        return player.take_damage(self.damage)
    
    def display_stats(self):
        print(f"\n=== {self.name} ===")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Damage: {self.damage}")

def generate_math_problem(difficulty):
    if difficulty == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
        problem = f"{a} {op} {b}"
        answer = eval(problem)
        return problem, answer
    elif difficulty == "medium":
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        op = random.choice(["+", "-", "*"])
        problem = f"{a} {op} {b}"
        answer = eval(problem)
        return problem, answer
    else:  # hard
        a = random.randint(10, 20)
        b = random.randint(1, 10)
        op = random.choice(["*", "//"])
        problem = f"{a} {op} {b}"
        answer = eval(problem)
        return problem, answer

def battle(player, monster):
    print(f"\n⚔️ A wild {monster.name} (Level {monster.level}) appears! ⚔️")
    
    while True:
        print("\nWhat will you do?")
        print("1. Attack with spell")
        print("2. Use health potion (heals 20 HP)")
        print("3. Try to flee")
        
        choice = input("Choose an action (1-3): ")
        
        if choice == "1":
            print("\nChoose a spell:")
            spells = list(player.spells.keys())
            for i, spell in enumerate(spells, 1):
                print(f"{i}. {spell} ({player.spells[spell]['difficulty']} math)")
            
            spell_choice = input("Select a spell (1-3): ")
            try:
                spell = spells[int(spell_choice)-1]
                difficulty = player.spells[spell]["difficulty"]
                damage = player.spells[spell]["damage"]
                
                problem, answer = generate_math_problem(difficulty)
                print(f"\nSolve this math problem to cast {spell}:")
                print(f"What is {problem}?")
                
                try:
                    user_answer = int(input("Your answer: "))
                    if user_answer == answer:
                        print(f"\n✨ {spell} hits {monster.name} for {damage} damage! ✨")
                        if monster.take_damage(damage):
                            exp_gain = monster.level * 20
                            player.gain_exp(exp_gain)
                            return True
                    else:
                        print(f"\n❌ Incorrect! The answer was {answer}. Your spell fizzles!")
                except ValueError:
                    print("\nInvalid input! Spell failed!")
                
            except (IndexError, ValueError):
                print("\nInvalid spell choice!")
        
        elif choice == "2":
            player.heal(20)
        
        elif choice == "3":
            if random.random() < 0.5:  # 50% chance to flee
                print("\nYou successfully fled from battle!")
                return False
            else:
                print("\nYou failed to flee!")
        
        else:
            print("\nInvalid choice! Try again.")
            continue
        
        # Monster's turn if it's still alive
        if monster.hp > 0:
            if monster.attack(player):
                return False

def explore(player):
    locations = [
        "Enchanted Forest",
        "Mystic Mountains",
        "Ancient Ruins",
        "Dragon's Valley",
        "Wizard's Tower"
    ]
    
    current_location = random.choice(locations)
    print(f"\nYou are exploring {current_location}...")
    
    # Random events
    event = random.random()
    
    if event < 0.6:  # 60% chance of battle
        monster_level = max(1, player.level + random.randint(-1, 1))
        monsters = [
            "Goblin", "Skeleton", "Slime", "Wolf", "Orc",
            "Troll", "Dragonling", "Ghost", "Spider", "Bat"
        ]
        monster_name = random.choice(monsters)
        monster = Monster(monster_name, monster_level)
        return battle(player, monster)
    elif event < 0.8:  # 20% chance to find health potion
        print("\nYou found a health potion! +20 HP")
        player.heal(20)
        return True
    else:  # 20% chance nothing happens
        print("\nYou explore the area but find nothing of interest.")
        return True

def main():
    print("""
    ============================
       WELCOME TO MATH QUEST    
    ============================
    """)
    
    player_name = input("Enter your wizard's name: ")
    player = Player(player_name)
    
    print(f"\nWelcome, {player_name}! Let the adventure begin!")
    
    while True:
        player.display_stats()
        
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Rest (heal to full HP)")
        print("3. Quit game")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            if not explore(player):
                print("\nGame Over! Better luck next time.")
                break
        elif choice == "2":
            player.heal(player.max_hp - player.hp)
        elif choice == "3":
            print("\nThanks for playing Math Quest!")
            break
        else:
            print("\nInvalid choice! Please try again.")
        
        time.sleep(1)  # Pause for readability

if __name__ == "__main__":
    main()

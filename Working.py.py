import random
import re
from functools import wraps

# ============================================
# PART 1: Decorator – Magical boost
# ============================================

def magic_boost(factor):
    """Decorator that multiplies the return value of a method by factor"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, (int, float)):
                return result * factor
            return result
        return wrapper
    return decorator


# ============================================
# PART 2 & 3: Iterator & Generator – Creature powers
# ============================================

def weak_powers(creature):
    """Generator that yields only power names shorter than 5 letters"""
    for power in creature.powers:
        if len(power) < 5:
            yield power


def validate_power_name(power_name: str) -> bool:
    """Regex validation: only lowercase letters, optionally hyphens or spaces"""
    pattern = r"^[a-z\s\-]+$"
    return bool(re.match(pattern, power_name))


# ============================================
# Problem 1: Inheritance Hierarchy
# ============================================

class Creature:
    """Base class for all creatures in the magical academy"""
    def __init__(self, name: str, health: int = 100):
        self.name = name
        self.health = health
        self.potion = None  # Association attribute, starts as None
        self.powers = ["fire", "heal", "lightning"]  # Iterator powers
        self._power_index = 0  # For iterator support

    def __iter__(self):
        """Make Creature an iterator over its powers"""
        self._power_index = 0
        return self

    def __next__(self):
        """Yield the next power in the list"""
        if self._power_index < len(self.powers):
            power = self.powers[self._power_index]
            self._power_index += 1
            return power
        else:
            raise StopIteration

    def add_power(self, power_name: str):
        """Add a new power after validating the name"""
        if validate_power_name(power_name):
            self.powers.append(power_name)
            print(f"✨ {self.name} learned a new power: '{power_name}'")
        else:
            print(f"❌ Invalid power name: '{power_name}'. Only lowercase letters, hyphens, and spaces allowed.")

    def get_weak_powers(self):
        """Return a generator of weak powers (< 5 letters)"""
        return weak_powers(self)

    def take_damage(self, damage: int):
        """Reduce health based on damage"""
        self.health = max(0, self.health - damage)

    def is_alive(self) -> bool:
        """Return True if health is greater than 0"""
        return self.health > 0

    def attack(self):
        """Method to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement this method")

    def drink_potion(self, potion):
        """Drink the potion and restore health"""
        if self.potion:
            self.health += potion.potency
            print(f"✨ {self.name} drinks {self.potion.name}. Health increased by {potion.potency}. Current health: {self.health}")
            self.potion = None  # Consume the potion


class Dragon(Creature):
    """Dragon subclass inheriting Creature, with damage reduction if fire_power is high"""
    def __init__(self, name: str, health: int = 100, fire_power: int = 0):
        super().__init__(name, health)
        self.fire_power = fire_power

    def take_damage(self, damage: int):
        """Apply custom damage reduction if fire_power > 30"""
        if self.fire_power > 30:
            actual_damage = max(0, damage - 10)
            print(f"🔥 {self.name}'s flame shield blocks 10 damage! Took {actual_damage} damage.")
        else:
            actual_damage = damage
        super().take_damage(actual_damage)

    @magic_boost(1.5)
    def attack(self) -> int:
        """Dragon attack implementation (boosted by 1.5x)"""
        damage = self.fire_power + random.randint(5, 10)
        print(f"🐉 {self.name} breathes fire! Base damage: {damage}. Boosted damage: {damage * 1.5:.0f}")
        return damage


class Unicorn(Creature):
    """Unicorn subclass with a healing ability"""
    def __init__(self, name: str, health: int = 100, heal_amount: int = 15):
        super().__init__(name, health)
        self.heal_amount = heal_amount

    def heal(self):
        """Restore health by heal amount"""
        self.health += self.heal_amount
        print(f"🦄 {self.name} uses heal. Health increased by {self.heal_amount}. Current health: {self.health}")

    def attack(self) -> int:
        """Unicorn attack implementation with fixed gentle damage"""
        damage = 12
        print(f"🦄 {self.name} charges gently. Deals {damage} damage.")
        return damage


# Problem 2: Polymorphism with Attacks

class Phoenix(Creature):
    """Phoenix subclass with flame health and revival mechanism"""
    def __init__(self, name: str, health: int = 100, flame_health: int = 40):
        super().__init__(name, health)
        self.flame_health = flame_health

    def attack(self) -> int:
        """Phoenix attack implementation using random values"""
        damage = random.randint(10, 25)
        print(f"🦅 {self.name} uses flame strike. Deals {damage} damage.")
        return damage

    def take_damage(self, damage: int):
        """Phoenix revives when health hits 0 if flame health > 0"""
        super().take_damage(damage)
        if self.health <= 0 and self.flame_health > 0:
            self.health = 30
            self.flame_health -= 20
            print(f"✨ {self.name} revives from ashes! Health is now {self.health}.")


# Problem 3: Association with Potions

class MagicPotion:
    """Potion class representing items creature can use"""
    def __init__(self, name: str, effect: str, potency: int):
        self.name = name
        self.effect = effect
        self.potency = potency

    def use(self):
        """Display potion use information"""
        print(f"🧪 Potion {self.name} used.")


# Bonus: Goblin Class

class Goblin(Creature):
    """Goblin subclass that can steal potions"""
    def __init__(self, name: str, health: int = 50):
        super().__init__(name, health)

    def attack(self) -> int:
        """Goblin attack implementation with random damage"""
        damage = random.randint(5, 12)
        print(f"👺 {self.name} strikes with a dagger. Deals {damage} damage.")
        return damage

    def steal_potion(self, target: Creature):
        """Steal potion from another creature"""
        if target.potion is not None:
            self.potion = target.potion
            target.potion = None
            print(f"👺 {self.name} stole the {self.potion.name} from {target.name}!")
        else:
            print(f"👺 {self.name} tried to steal, but {target.name} has no potion.")


# Problem 4: Battle Simulator

class Battle:
    """Battle class to simulate the combat between two creatures"""
    def __init__(self, fighter1: Creature, fighter2: Creature):
        self.fighter1 = fighter1
        self.fighter2 = fighter2

    def fight_rounds(self, num_rounds: int):
        """Simulate rounds of battle"""
        print(f"\n===== ⚔️ Battle begins: {self.fighter1.name} vs {self.fighter2.name} ⚔️ =====")

        potions = [
            MagicPotion("Healing Potion", "Restores 20 health", 20),
            MagicPotion("Strength Potion", "Boosts attack", 10)
        ]
        # Association: fighters hold a random potion
        self.fighter1.potion = random.choice(potions)
        self.fighter2.potion = random.choice(potions)
        print(f"-> {self.fighter1.name} gets a {self.fighter1.potion.name}")
        print(f"-> {self.fighter2.name} gets a {self.fighter2.potion.name}\n")

        for r in range(1, num_rounds + 1):
            print(f"--- Round {r} ---")
            
            # Creature 1 attacks Creature 2
            dmg1 = self.fighter1.attack()
            self.fighter2.take_damage(dmg1)
            print(f"    -> {self.fighter2.name} remaining health: {self.fighter2.health}")
            if not self.fighter2.is_alive():
                print(f"🏆 {self.fighter2.name} is down! {self.fighter1.name} wins!")
                break
                
            # Creature 2 attacks Creature 1
            dmg2 = self.fighter2.attack()
            self.fighter1.take_damage(dmg2)
            print(f"    -> {self.fighter1.name} remaining health: {self.fighter1.health}")
            if not self.fighter1.is_alive():
                print(f"🏆 {self.fighter1.name} is down! {self.fighter2.name} wins!")
                break

            # Drink potions randomly
            if self.fighter1.potion and random.random() > 0.5:
                self.fighter1.drink_potion(self.fighter1.potion)
            if self.fighter2.potion and random.random() > 0.5:
                self.fighter2.drink_potion(self.fighter2.potion)

        print("\n===== Battle over. =====\n")


# Execution and Testing

if __name__ == "__main__":
    print(">>> Testing Problem 1: Inheritance")
    d_test = Dragon("Ignis", 100, 35)
    d_test.take_damage(25)
    print("-" * 30)

    print(">>> Testing Problem 2: Polymorphism")
    creatures = [
        Dragon("Drogon", 100, 32),
        Unicorn("Uni", 100, 15),
        Phoenix("Fawkes", 100, 40)
    ]
    for c in creatures:
        c.attack()
    print("-" * 30)

    print(">>> Testing Problem 3: Association")
    u_test = Unicorn("Pegasus", 100, 15)
    u_test.potion = MagicPotion("Small Potion", "Restore", 10)
    u_test.drink_potion(u_test.potion)
    print("-" * 30)

    print(">>> Testing Problem 4: Battle Simulator")
    b = Battle(Dragon("Charizard", 100, 32), Phoenix("Articuno", 100, 35))
    b.fight_rounds(3)
    print("-" * 30)

    print(">>> Testing Bonus: Goblin stealing")
    goblin = Goblin("Grum")
    goblin.steal_potion(b.fighter1)
    print("-" * 50)

    # ========== NEW TESTS ==========
    print("\n>>> Testing PART 1: Decorator @magic_boost")
    dragon_boost = Dragon("Flamebringer", 100, 40)
    boosted_damage = dragon_boost.attack()  # Returns boosted damage
    print("-" * 50)

    print("\n>>> Testing PART 2: Iterator – Creature powers")
    phoenix = Phoenix("Solaris", 100, 35)
    print(f"Powers of {phoenix.name}: {phoenix.powers}")
    print("Iterating through powers:")
    for power in phoenix:
        print(f"  ⚡ {power}")
    print("-" * 50)

    print("\n>>> Testing PART 3: Generator – Weak powers")
    unicorn_powers = Unicorn("Stardust", 100, 20)
    print(f"All powers of {unicorn_powers.name}: {unicorn_powers.powers}")
    print("Weak powers (< 5 letters):")
    for weak_power in unicorn_powers.get_weak_powers():
        print(f"  🌟 {weak_power}")
    print("-" * 50)

    print("\n>>> Testing PART 4: Regex – Validate power names")
    test_creature = Goblin("TestGoblin")
    
    valid_names = ["fire", "ice-bolt", "heal spell", "lightning"]
    invalid_names = ["Fire", "ice_bolt", "123power", "heal!"]
    
    print(f"Valid power names to add:")
    for name in valid_names:
        test_creature.add_power(name)
    
    print(f"\nInvalid power names to add:")
    for name in invalid_names:
        test_creature.add_power(name)
    
    print(f"\nFinal powers of {test_creature.name}: {test_creature.powers}")
    print("-" * 50)
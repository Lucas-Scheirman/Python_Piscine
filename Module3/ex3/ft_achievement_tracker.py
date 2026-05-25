import random

ALL_ACHIEVEMENTS = [
    "Boss Slayer",
    "Speed Runner",
    "Untouchable",
    "World Savior",
    "Survivor",
    "First Steps",
    "Crafting Genius",
    "Strategist",
    "Master Explorer",
    "Collector Supreme",
    "Unstoppable",
    "Treasure Hunter",
    "Sharp Mind",
    "Hidden Path Finder"
]


def gen_player_achievements() -> set[str]:
    return set(
        random.sample(
            ALL_ACHIEVEMENTS,
            random.randint(
                1,
                len(ALL_ACHIEVEMENTS))))


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()

    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}\n")
    all_achievements = alice | bob | charlie | dylan
    print(f"All distinct achievements: {all_achievements}\n")
    print(f"Common achievements: {alice & bob & charlie & dylan}\n")
    print(f"Only Alice has: {alice - bob - charlie - dylan}")
    print(f"Only Bob has: {bob - alice - charlie - dylan}")
    print(f"Only Charlie has: {charlie - alice - bob - dylan}")
    print(f"Only Dylan has: {dylan - alice - bob - charlie}\n")
    print(f"Alice is missing: {all_achievements - alice}")
    print(f"Bob is missing: {all_achievements - bob}")
    print(f"Charlie is missing: {all_achievements - charlie}")
    print(f"Dylan is missing: {all_achievements - dylan}")

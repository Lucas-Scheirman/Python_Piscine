from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        result1 = spell1(target, power)
        result2 = spell2(target, power)
        return (result1, result2)
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        new_power = power * multiplier
        return base_spell(target, new_power)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def go_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return go_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    def go_spell(target: str, power: int) -> list:
        return [spell(target, power) for spell in spells]
    return go_spell


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def main() -> None:
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result1, result2 = combined("Dragon", 10)
    print(f"Combined spell result: {result1}, {result2}")

    print("Testing power amplifier...")
    power = 10
    multiplier = 3
    print(f"Original: {power}, Amplified: {power * multiplier}")

    print("Testing conditional caster...")
    guarded = conditional_caster(lambda t, p: p >= 20, fireball)
    print(f"Power 10: {guarded('Dragon', 10)}")
    print(f"Power 30: {guarded('Dragon', 30)}")

    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal])
    for result in sequence("Dragon", 15):
        print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

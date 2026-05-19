from collections.abc import Callable

def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        sort1 = spell1(target, power)
        sort2 = spell2(target, power)
        return (sort1, sort2)
    return combined


def power_amplifier(base_spell, multiplier):
    def amplified(target: str, power: int):
        new_power = power * multiplier
        sort = base_spell(target, new_power)
        return sort
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def go_spell(target: str, power: int):
        if condition(target, power):
            return spell(target, power)
        else:
            return f"Spell fizzled"
    return go_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    def go_spell(target: str, power: int):
        return [e(target,power) for e in spells]
    return go_spell



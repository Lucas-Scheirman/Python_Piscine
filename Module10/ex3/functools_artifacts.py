from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    all_operator = {"add": add, "multiply": mul, "max": max, "min": min}
    if not spells:
        return 0
    if operation not in all_operator:
        raise ValueError(f"Unknown operation: {operation}")
    return reduce(all_operator[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire": partial(base_enchantment, 50, "fire"),
        "ice": partial(base_enchantment, 50, "ice"),
        "lightning": partial(base_enchantment, 50, "lightning")
    }


@lru_cache
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


def spell_dispatcher() -> Callable:
    @singledispatch
    def cast(spell):
        return "Unknown spell type"

    @cast.register(int)
    def _(spell):
        return f"Damage spell: {spell} damage"

    @cast.register(str)
    def _(spell):
        return f"Enchantment: {spell}"

    @cast.register(list)
    def _(spell):
        return f"Multi-cast: {len(spell)} spells"

    return cast
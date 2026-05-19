from collections.abc import Callable

def mage_counter() -> Callable:
    count = 0

    def count_f() -> int:
        nonlocal count
        count += 1
        return count
    return count_f


def spell_accumulator(initial_power: int) -> Callable:
    count = initial_power

    def count_f(add_power) -> int:
        nonlocal count
        count += add_power
        return count
    return count_f


def enchantment_factory(enchantment_type: str) -> Callable:
    def add(item) -> str:
        return f"{enchantment_type} {item}"
    return add


def memory_vault() -> dict[str, Callable]:
    dico = {}

    def store(key: str, value) -> None:
        dico[key] = value

    def recall(key: str) -> str:
        if key in dico:
            return f"{dico[key]}"
        else:
            return "Memory not found"
    return {'store': store, 'recall': recall}

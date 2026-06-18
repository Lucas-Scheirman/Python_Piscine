from collections.abc import Callable


def mage_counter() -> Callable:
    count = 0

    def count_f() -> int:
        nonlocal count
        count += 1
        return count
    return count_f


def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def add_power(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return add_power


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item: str) -> str:
        return f"{enchantment_type} {item}"
    return enchant


def memory_vault() -> dict[str, Callable]:
    storage: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        storage[key] = value

    def recall(key: str) -> str:
        if key in storage:
            return f"{storage[key]}"
        return "Memory not found"
    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("Testing spell accumulator...")
    accumulator = spell_accumulator(100)
    print(f"Base 100, add 20: {accumulator(20)}")
    print(f"Base 100, add 30: {accumulator(30)}")

    print("Testing enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("Testing memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("Store 'secret' = 42")
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

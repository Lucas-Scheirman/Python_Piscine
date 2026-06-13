from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


def test_healing() -> None:
    factory = HealingCreatureFactory()
    creatures = [("base:", factory.create_base()),
                 ("evolved:", factory.create_evolved())]
    for label, creature in creatures:
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, HealCapability):
            print(creature.heal())


def test_transform() -> None:
    factory = TransformCreatureFactory()
    creatures = [("base:", factory.create_base()),
                 ("evolved:", factory.create_evolved())]
    for label, creature in creatures:
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())


if __name__ == "__main__":
    try:
        print("Testing Creature with healing capability")
        test_healing()
        print("\nTesting Creature with transform capability")
        test_transform()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")

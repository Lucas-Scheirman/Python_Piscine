from ex0 import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    base1 = factory1.create_base()
    base2 = factory2.create_base()
    print(base1.describe())
    print("vs.")
    print(base2.describe())
    print("fight!")
    print(base1.attack())
    print(base2.attack())


if __name__ == "__main__":
    try:
        flame_factory = FlameFactory()
        aqua_factory = AquaFactory()

        print("Testing factory")
        test_factory(flame_factory)

        print("Testing factory")
        test_factory(aqua_factory)

        print("Testing battle")
        battle(flame_factory, aqua_factory)

    except Exception as e:
        print(f"An unexpected error occurred during the battle: {e}")

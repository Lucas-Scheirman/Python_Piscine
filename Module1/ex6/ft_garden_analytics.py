class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self._name = name
        if (height < 0.0):
            self._height = 0.0
        else:
            self._height = round(height, 1)
        if (days < 0):
            self._days = 0
        else:
            self._days = round(days)
        self._stats = Plant.Stats()

    def show(self) -> None:
        print(
            f"{self._name}:"
            f" {(self.get_height())}cm, "
            f"{self.get_age()} days old"
        )
        self._stats._show += 1

    def grow(self) -> None:
        self._height = round(self._height + 0.8, 1)
        self._stats._grow += 1

    def age(self) -> None:
        self._days += 1
        self._stats._age += 1

    def set_height(self, height: float) -> None:
        if height < 0:
            print(
                f"{self._name}: "
                f"Error, height can't be negative\n"
                f"Height update rejected"
            )
        else:
            self._height = height
            print(f"Height updated: {self.get_height()}cm")

    def set_age(self, days: int) -> None:
        if days < 0:
            print(
                f"{self._name}: "
                f"Error, age can't be negative\n"
                f"Age update rejected"
            )
        else:
            self._days = days
            print(f"Age updated: {self.get_age()} days")

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._days

    @staticmethod
    def is_older_than_year(days: int) -> bool:
        return days > 365

    @classmethod
    def anonymous_plant(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    class Stats:
        def __init__(self) -> None:
            self._grow = 0
            self._age = 0
            self._show = 0

        def display(self) -> None:
            print(
                f"Stats: {self._grow} grow, "
                f"{self._age} age, "
                f"{self._show} show"
            )


class Flower(Plant):
    def __init__(
        self, name: str, height: float, days: int, color: str
    ) -> None:
        super().__init__(name, height, days)
        self._color = color
        self._bloomed = False

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if not self._bloomed:
            print(f"{self._name} has not bloomed yet")
        else:
            print(f"{self._name} is blooming beautifully!")

    def grow(self) -> None:
        self._height = round(self._height + 8.0, 1)
        self._stats._grow += 1

    def bloom(self) -> None:
        self._bloomed = True


class Tree(Plant):
    def __init__(
        self, name: str, height: float, days: int, trunk_diameter: float
    ) -> None:
        super().__init__(name, height, days)
        self._trunk_diameter = trunk_diameter
        self._stats: "Tree.Stats" = Tree.Stats()

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter}cm")

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self.get_height()}cm long and "
            f"{self._trunk_diameter}cm wide."
        )
        self._stats._produce_shade_count += 1

    class Stats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._produce_shade_count = 0

        def display(self) -> None:
            super().display()
            print(f"{self._produce_shade_count} shade")


class Vegetable(Plant):
    def __init__(
        self, name: str, height: float, days: int, harvest_season: str
    ) -> None:
        super().__init__(name, height, days)
        self._harvest_season = harvest_season
        self._nutritional_value = 0.0

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {round(self._nutritional_value)}")

    def grow(self) -> None:
        self._height = round(self._height + 2.1, 1)
        self._nutritional_value = round(self._nutritional_value + 0.5, 1)
        self._stats._grow += 1

    def age(self) -> None:
        super().age()
        self._nutritional_value = round(self._nutritional_value + 0.5)


class Seed(Flower):
    def __init__(self, name: str, height: float, days: int,
                 color: str) -> None:
        super().__init__(name, height, days, color)
        self._seeds = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._seeds}")

    def grow(self) -> None:
        self._height = round(self._height + 30.0, 1)
        self._stats._grow += 1

    def age(self) -> None:
        self._days += 20
        self._stats._age += 1


def display_stats(plant: Plant) -> None:
    plant._stats.display()


def main() -> None:
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print("[statistics for Rose]")
    display_stats(rose)

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[statistics for Oak]")
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("[statistics for Oak]")
    display_stats(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age()
    sunflower.bloom()
    sunflower.show()
    print("[statistics for Sunflower]")
    display_stats(sunflower)

    print("=== Anonymous")
    unknown = Plant.anonymous_plant()
    unknown.show()
    print("[statistics for Unknown plant]")
    display_stats(unknown)


if __name__ == "__main__":
    main()

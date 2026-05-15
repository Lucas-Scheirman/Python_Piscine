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

    def show(self) -> None:
        print(
            f"{self._name}:"
            f" {self.get_height()}cm, "
            f"{self.get_age()} days old"
        )

    def grow(self) -> None:
        self._height = round(self._height + 0.8, 1)

    def age(self) -> None:
        self._days += 1

    def set_height(self, height: float) -> None:
        if height < 0:
            print(
                f"{self._name}: "
                f"Error, height can't be negative\n"
                f"Height update rejected"
            )
        else:
            self._height = round(height, 1)
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

    def bloom(self) -> None:
        self._bloomed = True


class Tree(Plant):
    def __init__(
        self, name: str, height: float, days: int, trunk_diameter: float
    ) -> None:
        super().__init__(name, height, days)
        self._trunk_diameter = round(trunk_diameter, 1)

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter}cm")

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self.get_height()}cm long and "
            f"{self._trunk_diameter}cm wide."
        )


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
        self._nutritional_value = round(self._nutritional_value + 0.5)

    def age(self) -> None:
        super().age()
        self._nutritional_value = round(self._nutritional_value + 0.5)


if __name__ == "__main__":
    rose = Flower("Rose", 15.0, 10, "red")
    oak = Tree("Oak", 200.0, 365, 5.0)
    tomato = Vegetable("Tomato", 5.0, 10, "April")

    print("=== Garden Plant Types ===")
    print("=== Flower")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print("=== Tree")
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print("=== Vegetable")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for i in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()

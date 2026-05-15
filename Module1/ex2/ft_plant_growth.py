class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self.height = round(height, 1)
        self.days = round(days)

    def show(self) -> None:
        print(
            f"{self.name}: "
            f"{round(self.height, 1)}cm, "
            f"{self.days} days old"
        )

    def grow(self) -> None:
        self.height = round(self.height + 0.8, 1)

    def age(self) -> None:
        self.days += 1


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30)
    start_height = rose.height
    print("=== Garden Plant Growth ===")
    rose.show()
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.age()
        rose.grow()
        rose.show()
    print(f"Growth this week: {round(rose.height - start_height, 1)}cm")

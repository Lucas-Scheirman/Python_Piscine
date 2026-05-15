class Plant:
    def __init__(self, name: str, height: float, days: int) -> None:
        self.name = name
        self.height = round(height, 1)
        self.days = round(days)

    def show(self) -> None:
        print(
            f"Created: {self.name}: "
            f"{round(self.height, 1)}cm, "
            f"{self.days} days old"
        )

    def grow(self) -> None:
        self.height = round(self.height + 0.8, 1)

    def age(self) -> None:
        self.days += 1


if __name__ == "__main__":
    plants = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]
    print("=== Plant Factory Output ===")
    for plant in plants:
        plant.show()

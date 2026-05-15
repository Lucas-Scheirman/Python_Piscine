class GardenError(Exception):
    def __init__(self, msg: str = "Unknown Garden error") -> None:
        super().__init__(msg)


class PlantError(GardenError):
    def __init__(self, msg: str = "Unknown plant error") -> None:
        super().__init__(msg)


def water_plant(plante_name: str) -> None:
    if (plante_name != plante_name.capitalize()):
        raise PlantError(f"Invalid plant name to water: '{plante_name}'")
    print(f"Watering {plante_name}: [OK]")


def test_watering_system() -> None:
    print("Testing valid plants...\nOpening watering system")
    try:
        water_plant("Tomato")
        water_plant("Lettuce")
        water_plant("Carotts")

    except PlantError as e:
        print(e)
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system\n")
    print("Testing invalid plants...\nOpening watering system")
    try:
        water_plant("Tomato")
        water_plant("lettuce")

    except PlantError as e:
        print(e)
        print(".. ending tests and returning to main")
        return
    finally:
        print("Closing watering system\n")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    test_watering_system()
    print("Cleanup always happens, even with errors!")

from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self) -> None:
        self._name = ""
        self._type = ""

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self._name} is a {self._type} type Creature"


class Flameling(Creature):
    def __init__(self) -> None:
        self._name = "Flameling"
        self._type = "Fire"

    def attack(self) -> str:
        return "Flameling uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        self._name = "Pyrodon"
        self._type = "Fire/Flying"

    def attack(self) -> str:
        return "Pyrodon uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self) -> None:
        self._name = "Aquabub"
        self._type = "Water"

    def attack(self) -> str:
        return "Aquabub uses Water Gun!"


class Torragon(Creature):
    def __init__(self) -> None:
        self._name = "Torragon"
        self._type = "Water"

    def attack(self) -> str:
        return "Torragon uses Hydro Pump!"

import elements
import alchemy.elements


def healing_potion() -> str:
    return (
        f"Healing potion brewed with '{alchemy.elements.create_earth()}'"
        f" and '{alchemy.elements.create_air()}'"
    )


def strength_potion() -> str:
    return (
        f"Strength potion brewed with '{elements.create_fire()}'"
        f" and '{elements.create_water()}'"
    )

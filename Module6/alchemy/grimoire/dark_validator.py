from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    if any(word in ingredients.lower() for word in allowed):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"

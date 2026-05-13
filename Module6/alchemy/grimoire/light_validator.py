def validate_ingredients(ingredients: str) -> str:
    allowed = ["earth", "air", "fire", "water"]
    if any(word in ingredients.lower() for word in allowed):
        return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"

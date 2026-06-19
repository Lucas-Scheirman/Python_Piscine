def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    powerful_enough = filter(lambda x: x["power"] >= min_power, mages)
    return list(powerful_enough)


def spell_transformer(spells: list[str]) -> list[str]:
    transformed = map(lambda x: f"* {x} *", spells)
    return list(transformed)


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    max_power = max(mages, key=lambda x: x["power"])["power"]
    min_power = min(mages, key=lambda x: x["power"])["power"]
    total = sum(map(lambda x: x["power"], mages))
    avg_power = round(total / len(mages), 2)

    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power,
    }


def main() -> None:
    artifacts = [
        {"name": "Crystal Orb", "power": 85, "type": "orb"},
        {"name": "Fire Staff", "power": 92, "type": "staff"},
        {"name": "Ice Wand", "power": 70, "type": "wand"},
    ]
    mages = [
        {"name": "Alex", "power": 80, "element": "fire"},
        {"name": "Jordan", "power": 60, "element": "water"},
        {"name": "Riley", "power": 95, "element": "air"},
    ]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    first, second = sorted_artifacts[0], sorted_artifacts[1]
    print(
        f"{first['name']} ({first['power']} power) comes before "
        f"{second['name']} ({second['power']} power)"
    )

    print("Testing power filter...")
    strong = power_filter(mages, 70)
    print(f"Mages with power >= 70: {[m['name'] for m in strong]}")

    print("Testing spell transformer...")
    print(" ".join(spell_transformer(["fireball", "heal", "shield"])))

    print("Testing mage stats...")
    print(mage_stats(mages))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")

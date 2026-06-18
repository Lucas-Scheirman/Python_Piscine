def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[dict]) -> dict:
    return {
        "max_power": max(mages, key=lambda x: x["power"])["power"],
        "min_power": min(mages, key=lambda x: x["power"])["power"],
        "avg_power": round(
            sum(map(lambda x: x["power"], mages)) / len(mages), 2
        ),
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

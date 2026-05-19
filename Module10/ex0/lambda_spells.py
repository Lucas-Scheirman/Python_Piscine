def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts,key=lambda x: x["power"],reverse=True)
def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x : x["power"] >= min_power,mages))
def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* "+ x + " *",spells))
def mage_stats(mages: list[dict]) -> dict:
    return {"max_power": max(mages, key = lambda x : x["power"])["power"],"min_power": min(mages, key = lambda x : x["power"])["power"],
            "avg_power":round(sum(map(lambda x: x["power"],mages)) / len(mages),2)}
from ex0 import FlameFactory, AquaFactory
from ex0.factory import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)
from ex2.strategy import BattleStrategy


def run_tournament(opponents:
                   list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    creatures = [(factory.create_base(), strategy)
                 for factory, strategy in opponents]
    try:
        for i in range(len(creatures)):
            for j in range(i + 1, len(creatures)):
                creature1, strategy1 = creatures[i]
                creature2, strategy2 = creatures[j]
                print("\n* Battle *")
                print(creature1.describe())
                print("vs.")
                print(creature2.describe())
                print("now fight!")
                strategy1.act(creature1)
                strategy2.act(creature2)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


if __name__ == "__main__":
    try:
        print("Tournament 0 (basic)")
        print("[ (Flameling+Normal), (Healing+Defensive) ]")
        run_tournament([
            (FlameFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
        ])

        print("\nTournament 1 (error)")
        print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
        run_tournament([
            (FlameFactory(), AggressiveStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
        ])

        print("\nTournament 2 (multiple)")
        print(
            "[ (Aquabub+Normal), (Healing+Defensive), "
            "(Transform+Aggressive) ]"
        )
        run_tournament([
            (AquaFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
            (TransformCreatureFactory(), AggressiveStrategy()),
        ])
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")

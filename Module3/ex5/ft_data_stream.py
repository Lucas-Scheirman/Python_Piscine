import random
from typing import Generator

players = ["alice", "bob", "charlie", "dylan"]
actions = ["run", "eat", "sleep", "grab",
           "move", "climb", "swim", "release", "use"]


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(liste_tuple: list[tuple[str, str]]) -> Generator[tuple[str, str], None, None]:
    while liste_tuple:
        yield (liste_tuple.pop(random.randint(0, len(liste_tuple) - 1)))


if __name__ == "__main__":
    gen_1 = gen_event()
    for i in range(1000):
        event = next(gen_1)
        print(f"Event {i}: Player {event[0]} did action {event[1]}")

    list_tuple = []
    gen_2 = gen_event()
    for i in range(10):
        list_tuple.append(next(gen_2))
    print(f"Built list of 10 events: {list_tuple}")

    for event in consume_event(list_tuple):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {list_tuple}")

import random

if __name__ == "__main__":
    players = ['Alice', 'bob', 'Charlie', 'dylan',
               'Emma', 'Gregory', 'john', 'kevin', 'Liam']

    print("=== Game Data Alchemist ===")
    print(f"Initial list of players: {players}")
    capitalized = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {capitalized}")
    already_capitalized = [
        name for name in players if name == name.capitalize()]
    print(f"New list of capitalized names only: {already_capitalized}")
    scores = {name: random.randint(1, 1000) for name in capitalized}
    print(f"Score dict: {scores}")
    average = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average}")
    high_scores = {name: score for name,
                   score in scores.items() if score > average}
    print(f"High scores: {high_scores}")

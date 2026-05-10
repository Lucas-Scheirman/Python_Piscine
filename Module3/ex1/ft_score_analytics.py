import sys

if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    score_processed = []
    total_player = len(sys.argv)
    total_score = 0
    for i in sys.argv[1:]:
        try:
            score_processed.append(int(i))
            total_score += int(i)
        except ValueError:
            print(f"Invalid parameter: '{i}'")

    if len(score_processed) == 0:
        print(
            f"No scores provided. Usage: python3 "
            f"{sys.argv[0]} <score1> <score2> ...\n")
    else:
        print(f"Scores processed: {score_processed}")
        print(f"Total players: {len(score_processed)}")
        print(f"Total score: {total_score}")
        print(f"Average score: {total_score / len(score_processed)}")
        print(f"High score: {max(score_processed)}")
        print(f"Low score: {min(score_processed)}")
        print(f"Score range: {max(score_processed) - min(score_processed)}\n")

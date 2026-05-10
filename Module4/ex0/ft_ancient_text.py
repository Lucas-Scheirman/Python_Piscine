import sys

if __name__ == "__main__":
    n = len(sys.argv)
    if n != 2:
        print(f"Usage: {sys.argv[0]} <file>")
    else:
        print("=== Cyber Archives Recovery ===")
        print(f"Accessing file '{sys.argv[1]}'")
        try:
            file = open(sys.argv[1], "r")
            text = file.read()
            print("---\n")
            print(text)
            print("\n")
            print("---")
            file.close()
            print(f"File '{sys.argv[1]}' closed.")
        except Exception as e:
            print(f"Error opening file '{sys.argv[1]}': {e}\n")

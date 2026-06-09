import sys

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Usage: {sys.argv[0]} <file>")
        else:
            print("=== Cyber Archives Recovery ===")
            print(f"Accessing file '{sys.argv[1]}'")
            file = open(sys.argv[1], "r")
            text = file.read()
            print("---\n")
            print(text)
            print("\n")
            print("---")
            file.close()
            print(f"File '{sys.argv[1]}' closed.")
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error opening file '{sys.argv[1]}': {e}\n")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nKeyboard interrupt by user")
        sys.exit(1)

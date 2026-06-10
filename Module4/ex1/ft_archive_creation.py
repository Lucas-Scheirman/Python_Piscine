import sys


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError(f"Usage: {sys.argv[0]} <file>")
        else:
            print("=== Cyber Archives Recovery & Preservation ===")
            print(f"Accessing file '{sys.argv[1]}'")
            try:
                file = open(sys.argv[1], "r")
                text = file.read()
                print("---\n")
                print(text)
                print("---")
                file.close()
                print(f"File '{sys.argv[1]}' closed.")
                print("Transform data:")
                print("---")
                list_line = text.split("\n")
                list_line = [line + "#" for line in list_line]
                for line in list_line:
                    print(line)
                print("---")
            except Exception as e:
                print(f"Error opening file '{sys.argv[1]}': {e}\n")
                sys.exit(1)
            file_name = input("Enter new file name (or empty): ")
            if not file_name:
                print("Not saving data.")
            else:
                try:
                    print(f"Saving data to '{file_name}'")
                    file = open(file_name, "w")
                    file.write("\n".join(list_line))
                    file.close()
                    print(f"Data saved in file '{file_name}'.")
                except Exception as e:
                    print(f"Error opening file '{file_name}': {e}")
                    sys.exit(1)
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nKeyboard interrupt by user")
        sys.exit(1)

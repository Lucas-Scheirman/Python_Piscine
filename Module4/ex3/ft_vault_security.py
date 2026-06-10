import sys


def secure_archive(file: str, mode: str = "r",
                   contain_write: str = "") -> tuple[bool, str]:
    try:
        if mode == "r":
            with open(file, mode) as f:
                file_txt = f.read()
            return (True, file_txt)
        else:
            with open(file, mode) as f:
                f.write(contain_write)
            return (True, "Content successfully written to file")
    except Exception as e:
        return (False, str(e))


if __name__ == "__main__":
    try:
        print("=== Cyber Archives Security ===\n")
        print("Using 'secure_archive' to read from a nonexistent file:")
        print(secure_archive("/not/existing/file", "r"))
        print("\n")
        print("Using 'secure_archive' to read from an inaccessible file:")
        print(secure_archive("/etc/master.passwd", "r"))
        print("\n")
        print("Using 'secure_archive' to read from a regular file:")
        result = secure_archive("ancient_fragment.txt", "r")
        print(result)
        print("\n")
        print("Using 'secure_archive' to write \
        previous content to a new file:")
        print(secure_archive("new_file.txt", "w", result[1]))
    except KeyboardInterrupt:
        print("keyboard interrupt by user")
        sys.exit(1)

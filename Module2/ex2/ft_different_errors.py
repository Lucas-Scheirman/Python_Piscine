def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        0/0
    elif operation_number == 2:
        open("/filenotexist")
    elif operation_number == 3:
        str_1 = "hi"
        str_1 += 1
    else:
        return


def test_error_types() -> None:
    print("Testing operation 0...")
    try:
        garden_operations(0)
        garden_operations(2)
    except (ValueError, FileNotFoundError) as e:
        print(f"Caught {type(e).__name__}: {e}")

    try:
        print("Testing operation 1...")
        garden_operations(1)
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}")

    try:
        print("Testing operation 2...")
        garden_operations(2)
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}")

    try:
        print("Testing operation 3...")
        garden_operations(3)
    except TypeError as e:
        print(f"Caught TypeError: {e}")

    print("Testing operation 4...")
    garden_operations(4)
    print("Operation completed successfully")
    print("All error types tested successfully!")


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    test_error_types()

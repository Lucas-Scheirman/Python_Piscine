def input_temperature(temp_str: str) -> int:
    result = int(temp_str)
    print(f"Temperature is now {result}°C\n")
    return result


def test_temperature() -> None:
    try:
        str_1 = "25"
        print(f"Input data is '{str_1}'")
        input_temperature(str_1)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    try:
        str_2 = "abc"
        print(f"Input data is '{str_2}'")
        input_temperature(str_2)
    except ValueError as e:
        print(f"Caught input_temperature error: {e}\n")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    print("=== Garden Temperature ===\n")
    test_temperature()

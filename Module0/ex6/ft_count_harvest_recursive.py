def print_days(days: int) -> None:
    if days != 1:
        print_days(days - 1)
    print("Day", days)


def ft_count_harvest_recursive() -> None:
    days = int(input("Days until harvest: "))
    if days != 0:
        print_days(days)
    print("Harvest time!")

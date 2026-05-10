import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        coords = input("Enter new coordinates as floats in format 'x,y,z':")
        coords_lst = coords.split(",")
        n = len(coords)
        error = False

        if n != 3:
            print("Invalid syntax")
            continue
        else:
            for i in coords_lst:
                try:
                    float(i)
                except ValueError as e:
                    print(f"Error on parameter '{i}': {e}")
                    error = True
                    break
        if not error:
            return (float(coords_lst[0]), float(coords_lst[1]), float(coords_lst[2]))


if __name__ == "__main__":
    print("=== Game Coordinate System ===\n")

    print("Get a first set of coordinates")
    pos1 = get_player_pos()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    print(
        f"Distance to center: {
            round(
                math.sqrt(
                    pos1[0]**2 +
                    pos1[1]**2 +
                    pos1[2]**2),
                4)}\n")

    print("Get a second set of coordinates")
    pos2 = get_player_pos()
    dist = math.sqrt((pos2[0] - pos1[0])**2 +
                     (pos2[1] - pos1[1])**2 + (pos2[2] - pos1[2])**2)
    print(f"Distance between the 2 sets of coordinates: {round(dist, 4)}")

import sys

if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory = {}
    for i in sys.argv[1:]:
        key_value = i.split(":")
        if (len(key_value) != 2):
            print(f"Error - invalid parameter '{key_value[0]}'")
        elif (key_value[0] in inventory):
            print(f"Redundant item '{key_value[0]}' - discarding")
        else:
            try:
                inventory[key_value[0]] = int(key_value[1])
            except ValueError as e:
                print(f"Quantity error for '{key_value[0]}': {e}")

    total = sum(inventory.values())
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(
        f"Total quantity of the {len(inventory.values())} items: {total}")
    for key, value in inventory.items():
        print(f"Item {key} represents {round((value / total) * 100, 1)}%")
    if not inventory:
        print("Item most abundant: None - inventory is empty!")
        print("Item least abundant: None - inventory is empty!")
    else:
        y = 0
        for k, v in inventory.items():
            if y == 0:
                max_item_v = v
                min_item_v = v
                max_item_k = k
                min_item_k = k
                y = 1
            if v > max_item_v:
                max_item_v = v
                max_item_k = k
            if v < min_item_v:
                min_item_v = v
                min_item_k = k
        print(f"Item most abundant: {max_item_k} with quantity {max_item_v}")
        print(f"Item least abundant: {min_item_k} with quantity {min_item_v}")
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")

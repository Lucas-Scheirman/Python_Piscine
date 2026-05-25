import sys

if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory = {}
    for i in sys.argv[1:]:
        key_value = i.split(":")
        if (len(key_value) != 2):
            print(f"Error - invalid parameter '{i}'")
        elif (key_value[0] in inventory):
            print(f"Redundant item '{key_value[0]}' - discarding")
        else:
            try:
                inventory[key_value[0]] = int(key_value[1])
            except ValueError as e:
                print(f"Quantity error for '{key_value[0]}': {e}")

    total_quantity = sum(inventory.values())
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(
        f"Total quantity of the {len(inventory.values())}"
        f" items: {total_quantity}")
    for key, value in inventory.items():
        print(f"Item {key} represents"
              f" {round((value / total_quantity) * 100, 1)}%")
    if not inventory:
        print("Item most abundant: None - inventory is empty!")
        print("Item least abundant: None - inventory is empty!")
    else:
        y = 0
        for key, value in inventory.items():
            if not y:
                max_item_v = value
                min_item_v = value
                max_item_k = key
                min_item_k = key
                y = 1
            if value > max_item_v:
                max_item_v = value
                max_item_k = key
            if value < min_item_v:
                min_item_v = value
                min_item_k = key
        print(f"Item most abundant: {max_item_k} with quantity {max_item_v}")
        print(f"Item least abundant: {min_item_k} with quantity {min_item_v}")
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")

# task link: https://www.youtube.com/shorts/d-mT0I96qhI


import itertools


class Item:
    def __init__(self, name: str, weight: int):
        self.name = name
        self.weight = weight


def get_max_load(items: list, max_load: int):
    # Check if only one item
    if len(items) == 1:
        trucks.append([items[0]])
        items.remove(items[0])
        return

    # Loop through all items
    combination = []
    for i in range(1, len(items) + 1):
        # Loop through all combinations
        for seq in itertools.combinations(items, i):
            combination.append([s for s in seq])

    items_max = []
    loading_max = 0
    # Loop through all combinations
    for item in combination:
        sum_of_items = sum([i.weight for i in item])

        # If loading reaches the max_load
        if sum_of_items == max_load:
            # Add items to the truck
            trucks.append([i for i in item])

            # Remove items from the list
            [items.remove(i) for i in item]
            return

        # Check the maximum loading possible
        if loading_max < sum_of_items <= max_load:
            loading_max = sum_of_items
            items_max = [i for i in item]

    # Add the maximum loading to the truck
    trucks.append(items_max)

    # Remove items from the list
    [items.remove(i) for i in items_max]


# Setup criteria
max_load_per_truck = 70
item1 = Item('Item 1', 10)
item2 = Item('Item 2', 20)
item3 = Item('Item 3', 30)
item4 = Item('Item 4', 40)
item5 = Item('Item 5', 50)

items = [item1, item2, item3, item4, item5]
trucks = []

# Loading the truck
while len(items) > 0:
    get_max_load(items, max_load_per_truck)

# Print result
print(f"Max load per truck: {max_load_per_truck}")
for i, t in enumerate(trucks, 1):
    print(f"Truck {i}: {[i.name for i in t]}. Loading in Trucks: {[i.weight for i in t]}")

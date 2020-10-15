from enum import Enum


class PizzaSize(Enum):
    small = {'base': 120, 'topping': 20}
    medium = {'base': 200, 'topping': 25}
    large = {'base': 280, 'topping': 30}
    jumbo = {'base': 500, 'topping': 50}

    def __str__(self):
        return self.name

    def price(self, ntoppings=0):
        return self.value['base'] + self.value['topping'] * ntoppings


class Pizza:
    """A pizza with a size and optional toppings."""

    def __init__(self, size: PizzaSize):
        if not isinstance(size, PizzaSize):
            raise TypeError('size must be a PizzaSize')
        self.size = size
        self.toppings = []

    def __str__(self):
        # create printable description of the pizza such as
        # "small pizza with muschroom" or "small plain pizza"
        description = str(self.size)
        if self.toppings:
            description += " pizza with " + ", ".join(self.toppings)
        else:
            description += " plain pizza"
        return description

    def get_price(self):
        """Price of pizza depends on size and number of toppings."""
        return self.size.price(len(self.toppings))

    def add_topping(self, topping):
        """Add a topping to the pizza"""
        if topping not in self.toppings:
            self.toppings.append(topping)

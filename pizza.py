class Pizza:
    """A pizza with a size and optional toppings."""

    def __init__(self, size):
        self.size = size
        self.toppings = []

    def getPrice(self):
        """Price of pizza depends on size and number of toppings."""
        if self.size == 'small':
            price = 120 + 20*len(self.toppings)
        elif self.size == 'medium':
            price = 200 + 25*len(self.toppings)
        elif self.size == 'large':
            price = 280 + 30*len(self.toppings)
        else:
            raise ValueError("Unknown pizza size "+self.size)
        return price
    
    def addTopping(self, topping):
        """Add a topping to the pizza"""
        if topping not in self.toppings:
            self.toppings.append(topping)


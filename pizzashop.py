from pizza import Pizza, PizzaSize


# This function shows a limitation on tool-assisted
# refactoring in a dynamic language like Python.
#
# When you rename the Pizza getPrice method to get_price,
# does it rename the method here?
# - if no type annotation on the pizza parameter, maybe not
# - if use type annotation ':Pizza' on the parameter, it should

def print_pizza(pizza: Pizza):
    """
    Print a description of a pizza, along with its price.
    """
    print(f"A {str(pizza)}")
    print("Price:", pizza.get_price())


# def test_pizza_sizes():
#     for size in PizzaSize:
#         print(size.name, "pizza price:", size.value)


if __name__ == "__main__":
    pizza = Pizza(PizzaSize.small)
    pizza.add_topping("mushroom")
    pizza.add_topping("tomato")
    pizza.add_topping("pinapple")
    print_pizza(pizza)

    pizza2 = Pizza(PizzaSize.medium)
    print_pizza(pizza2)

    pizza3 = Pizza(PizzaSize.large)
    pizza3.add_topping("seafood")
    print_pizza(pizza3)

    # test_pizza_sizes()

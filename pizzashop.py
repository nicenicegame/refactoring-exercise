from pizza import Pizza

#
# This function shows a limitation on tool-assisted
# refactoring in a dynamic language like Python.
#
# When you rename the Pizza get_price method,
# does it change here?
# - if no type annotation on the pizza parameter, maybe not
# - if a ':Pizza' type annotation on the parameter, it should

def print_pizza( pizza ):
    """
    Print a description of a pizza, along with its price.
    """
    # create printable description of the pizza
    if pizza.toppings:
        description = "pizza with "+ ", ".join(pizza.toppings)
    else:
        description = "plain pizza"
    print(f"A {pizza.size} {description}")
    print("Price {:6.2f}".format(pizza.getPrice()))


if __name__ == "__main__":
    pizza = Pizza('small')
    pizza.addTopping("mushroom")
    pizza.addTopping("tomato")
    pizza.addTopping("pinapple")
    print_pizza(pizza)

    pizza2 = Pizza("medium")
    print_pizza(pizza2)

    pizza3 = Pizza("large")
    pizza3.addTopping("seafood")
    print_pizza(pizza3)

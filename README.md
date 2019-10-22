## Refactoring Practice

Find some code in the Pizza class and pizzashop file that needs improvement, and perform refactorings.

Goals to achieve for the code are:

1. Replace magic numbers and strings with named constants.
    - refactor strings but don't bother adding constants for prices, because we have an better refactoring for prices.
2. Use consistent naming - rename symbols.
3. Make code more reusable by moving misplaced code to a better place (extract method and move method).
4. Replace "switch" (`if` ... `elif` ... `elif`) with object behavior.

### Background

Pizza describes a pizza with a size and optional toppings.  The price depends on size and number of toppings.  For example, large pizza is 280 Baht plus 30 Baht per topping.
```python
pizza = Pizza('large')
pizza.addTopping("muchroom")
pizza.addtopping("pineapple")
print("The price is", pizza.getPrice())
'The price is 340'
```
There are 2 files to start with:
```
pizza.py     - code for Pizza class
pizzashop.py - create some pizzas and print them. Use to verify code.
```

## 1. Replace String Literals with Named Constants

In the Pizza class replace 'small', 'medium', and 'large" with named constants.  Use your IDE's refactoring feature, not manual find and replace.

1. Select 'small' in Pizza.
   - VSCode: right click - Extract variable.
   - Pycharm: right click - Refactor - Extract - Constant
   - Pydev: Refactoring - Extract local variable. 
2. In my tests, none of the IDE did what I want. Edit your code to make them class-level constants:
    ```python
    class Pizza:
        SMALL = 'small'
        MEDIUM = 'medium'
        LARGE = 'large'
    
    # in "pizzashop":
    pizza = Pizza(Pizza.SMALL)
    ```
3. When you are done, the strings 'small', 'medium', 'large' should only appear **once** in the code.
4. Did your IDE also change the sizes in `pizzashop.py`?  If not, edit pizzashop.py and change sizes to references (`Pizza.SMALL`)
    ```python
    if __name__ == "__main__":
        pizza = Pizza(Pizza.SMALL)
        ...
        pizza2 = Pizza(Pizza.MEDIUM)
    ```
5. Run the code. Verify the results are the same.

## 2. Rename Symbols

1. `getPrice` is not a Python-style name.  Use refactoring to rename it to `get_price`.
    - VSCode: right-click on method name, choose "Rename Symbol"
    - Pycharm: right-click, Refactor -> Rename
    - Pydev: "Refactoring" menu -> Rename

2. Did the IDE rename `getPrice` in `print_pizza()`?
    - VSCode: no
    - Pycharm: yes. Notification of dynamic code in preview.
    - Pydev: yes (lucky guess)
    - This is a limitation of tools for dynamic languages. The tool can't be *sure* that the "pizza" parameter in `print_pizza` is *really* a Pizza.  To help it, use type annotations.

3. Undo the refactoring, so you have original `getPrice`.

4. Add a type annotation: `print_pizza(pizza: Pizza)`.
    - Then do Refactoring->Rename again.
    - Any difference?
    ```python
    def print_pizza( pizza: Pizza ):
        ...
        print("Price:", pizza.get_price())
    ```

5. Rename `addTopping` in Pizza to `add_topping`.  Did the IDE also rename it in pizzashop?
    - If not, rename it manually.
    - In this case, a smart IDE *can* infer that `addTopping` in pizzashop refers to Pizza.addTopping. Why?

6. Run the code. Verify the code works the same.

## 3. Extract Method and Move Method

`print_pizza` creates a string (`description`) to describe the pizza.  That is a poor location for this because:
- the description could be needed elsewhere in the application
- it relies on info about a Pizza that only the Pizza has

So, it should be the Pizza's job to describe itself.  This is also known as the *Information Expert* principle.

Try an *Extract Method* refactoring, followed by *Move Method*.

1. Select all statements in `print_pizza` that create the description **and** the preceding comments:
   ```python
    # create printable description of the pizza such as
    # "small pizza with muschroom" or "small plain pizza"
    description = pizza.size
    if pizza.toppings:
        description += " pizza with "+ ", ".join(pizza.toppings)
    else:
        description += " plain pizza"
    ```
2. Refactor:
    - VS Code: right click -> 'Extract Method'. Enter "describe" as method name.
    - PyCharm: right click -> Refactor -> Extract -> Method
    - PyCharm correctly suggests that "pizza" should be parameter, but incorrectly does not return anything. Fix it.
    - PyDev: Refactoring menu -> Extract method.  PyDev asks you if pizza should a parameter (correct), but incorrectly does not return anything.  Fix it.
    ```python
    def describe(pizza):
        # create printable description of the pizza such as
        # "small pizza with muschroom" or "small plain pizza"
        description = pizza.size
        if pizza.toppings:
            description += " pizza with "+ ", ".join(pizza.toppings)
        else:
            description += " plain pizza"
        return description
    ```
3. **Move Method:** We want the code for description to be in the Pizza class, so it can be used anywhere in the code.  There isn't an automatic refactoring for this, so do it yourself.  Cut the `describe(pizza)` method and paste it into pizza.py as the `__str__(self)` method. You should end up with this:
    ```python
    # In Pizza class:
    def __str__(self):
        # create printable description of the pizza such as
        # "small pizza with muschroom" or "small plain pizza"
        description = self.size
        if self.toppings:
            description += " pizza with "+ ", ".join(self.toppings)
        else:
            description += " plain pizza"
        return description
    ```
4. Back in `pizzashop.py`, modify the `print_pizza` to get the description from Pizza:
    ```python
    def print_pizza(pizza):
        description = str(pizza)
        print(f"A {descripton}")
        print("Price:", pizza.get_price())
    ```
5. **Eliminate Temp Variable** The `description` variable isn't necessary in such simple code, so refactor to eliminate it:
    ```python
    def print_pizza(pizza)
        print(f"A {str(pizza)}")
    ```
**Test:** Run the pizzashop code. Verify the results are the same.

## 4. Replace 'switch' with Call to Object Method

This is the most complex refactoring, but also yields big gains in code quality:
* code is simpler
* enables us to validate the pizza size in constructor
* prices and sizes can be changed or added without changing the Pizza class

The `get_price` method has a block like this:
```python
if self.size == Pizza.SMALL:
    price = ...
elif self.size == Pizza.MEDIUM:
    price = ...
elif self.size == Pizza.LARGE:
    price = ...
```
The pizza has to know pricing rules for each size, which makes the code complex.
An O-O approach would be to let the pizza sizes compute their own price.
Therefore, define a new datatype for pizza size with a `price()` method.

Python has an `Enum` type for this.
An "enum" is a type with a fixed set of values, which are static instances of the enum type.  Each enum member has a **name** and a **value**.

To define an enum for pizza sizes:
```python
from enum import Enum

class PizzaSize(Enum):
    # Enum members written as: name = value
    small = 120
    medium = 200
    large = 280

    def __str__(self):
        return self.name
```
Does this work?  Write some short code to try it.
```python
def test_pizza_sizes():
    for size in PizzaSize:
        print(size.name, "pizza price:",size.value)

if __name__ == "__main__":
    test_pizza_sizes()
```
It should print the pizza prices.  We *could* define a `price()` method:
```python
    def price(self):
        return self.value    # value of the enum member
```
But what about the price of toppings?

We need the number of toppings to compute pizza price,
so add a parameter to `price()`.  This avoids *coupling* it to the toppings.
```python
    def price(self,ntoppings=0):
        return self.value + ???*ntoppings
```
The per-topping price depends on size, so we need separate topping prices 
for each size.

Here are 2 solutions.  They both use the fact that the **value** of an enum member can be **anything**, not just a number or string.

1. Use a dict to specify base-price and topping price:
    ```python
    class PizzaSize(Enum):
        small = {'base': 120, 'topping': 20}
        medium = {'base': 180, 'topping': 25}
        large = {'base': 280, 'topping': 30}
        # in price() method use:
        # self.value['base'] + self.value['topping']*ntopping
    ```
2. Use a lambda to compute price.  Assigning lambda directly to enum members doesn't work as expected, so put them in a dict.
    ```python
    class PizzaSize(Enum):
        small = {'price': lambda ntopping: 120 + 20*ntopping}
        ...
        
        # self.value['price'] is a lambda (a function)
        # so you can invoke it using:
        # price = self.value['price'](ntopping)
    ```

Modify `pizzaSize.price(ntopping)` so it returns the pizza price with toppings.    
Use whichever solution you find **most easy to read**.
 
**Test** the code.

Then modify the Pizza class. Change `size` to use the PizzaSize enum and **delegate** pricing to it.
```python
# in Pizza class
   def get_price(self):
       return self.size.price( len(toppings) )

# In the pizzashop file:
pizza = Pizza( PizzaSize.small )
etc.
```
No "`if ... elif ... elif ...`"!


**Test** the code by running pizzashop. Verify results are same as before.

### Extensibility

Can you add a new pizza size *without* changing the Pizza class?
```python
class PizzaSize(Enum):
    ...
    jumbo: {"base": 500, "topping": 50}

# and in pizzashop.__main__:
pizza = Pizza(PizzaSize.jumbo)
```

### Type Safety

Since we eliminated the use of strings for sizes, we reduce the chance for error in creating a pizza, such as `Pizza("LARGE")`.

For better type safety, you can add an annotation and type check in the constructor:
```python
    def __init__(self, size: PizzaSize):
        if not isinstance(size, PizzaSize):
            raise TypeError('size must be a PizzaSize')
        self.size = size
```

## Further Refactoring

What if the price of each topping is different? 
Maybe "durian" topping costs more than "mushroom" topping.

There are two refactorings for this:

1. *Pass whole object instead of values* - instead of calling `size.price(len(toppings))`, use `size.price(toppings)`.
2. *Delegate to a Strategy* - pricing varies but sizes rarely change, so define a separate class to compute pizza price. 
    (Design principle: "*Separate the parts that vary from the parts that stay the same*")

## Reading

* Refactoring chapter in *Code Complete* 2nd Edition. Good overview but not much code.
* *Refactoring - Improving the Design of Existing Code* by Martin Fowler.  The bible on refactoring.  The first 4 chapters explain the fundamentals.
* https://refactoring.com. Online version of Fowler's book, very little detail.
* [Enumerations](https://docs.python.org/3/library/enum.html) in Python Library docs.

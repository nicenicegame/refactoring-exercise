## Refactoring Practice

Find some code in the Pizza class and pizzashop file that needs improvement, and perform refactorings.

Goals to achieve for the code are:

1. Replace magic numbers and strings with named constants.
    - refactor strings but don't bother adding constants for prices,  because we have an better refactoring for prices.
2. Use consistent naming - rename symbols.
3. Make code more reusable by moving misplaced code to a better place (extract method).
4. Replace "switch" (`if` ... `elif` ... `elif`) with object behavior.

### Background

Pizza describes a pizza with a size and optional toppings.  The price depends on size and number of toppings.  For example:
```python
pizza = Pizza('large')
pizza.addTopping("muchroom")
pizza.addtopping("pineapple")
print("The price is", pizza.getPrice())
```
There are 2 files to start with:
```
pizza.py     - code for Pizza class
pizzashop.py - create some pizzas and print them. Use to verify code.
```

## 1. Replace strings with Named Constants

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
    - this is a good reason not to use strings for sizes
5. Run the code. Verify the results are the same.

## 2. Rename Symbols

1. `getPrice` is not a Python-style name.  Use refactoring to rename it to `get_price`.
    - VSCode: right-click on method name, choose "Rename Symbol"
    - Pycharm: right-click, Refactor -> Rename
    - Pydev: "Refactoring" menu -> Rename

2. Did the IDE rename `getPrice` in `print_pizza()`?
    - VSCode: no
    - Pycharm: notification of dynamic code in preview. Interactively rename.
    - Pydev: yes (lucky guess)
    - This is a limitation of tools for dynamic languages: tool can't be *sure* that the "pizza" parameter in `print_pizza` is *really* a Pizza.  To help it, use type annotations.

3. Undo the refactoring, so you have original `getPrice`.

4. Add a type annotation: `print_pizza(pizza: Pizza)`.
    - Then do Refactoring->Rename again.
    - Any difference?

5. Rename `addTopping` in Pizza.  Did the IDE also rename it in pizzashop?

6. Run the code. Verify the results are the same.

## 3. Extract Method

`print_pizza` creates a string (`description`) to describe the pizza.  That is poor location for this because:
- same description could be needed elsewhere
- it relies on info about a Pizza that only the pizza has

So, it should be the Pizza's job to describe itself.  This is also known as the *Information Expert* principle.

1. Move the code that creates string description (but not the price) into Pizza class.
2. What method should use you?  How about `__str__`?
3. In print_pizza, invoke the method you just created, e.g. str(pizza).
3. Run the pizzashop code. Verify the results are the same.

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

Python has an `Enum` type for this:
```python
from enum import Enum

class PizzaSize(Enum):
    # write the sizes and their values 
    # one per line
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
        print(size, "pizza price:",size.value)

if __name__ == "__main__":
    test_pizza_sizes()
```
It should price the pizza prices.  So we *could* define:
```python
    def price(self):
        return self.value    # value of the enum member
```
But what about the price of toppings?

We only need the number of toppings to compute pizza price, 
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
        ...
        # in price() method use:
        # self.value['base'], self.value['topping']
    ```
2. Use a lambda to compute price.  Assigning lambda directly to enum members doesn't work as expected, so put them in a dict.
    ```python
    class PizzaSize(Enum):
        small = {'price': lambda ntopping: 120 + 20*ntopping}
        ...
        
        # self.value['price'] is a lambda (a function)
        # so you can invoke it using:
        #
        # price = self.value['price'](ntopping)
    ```

Modify `pizzaSize.price(ntopping)` to return the pizza price with toppings.    
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
No "`if size=... elif size=...`"!

**Test** the code by running pizzashop. Verify results are same as before.

### Extensibility

Can you add a new pizza size *without* changing the Pizza class?

## Further Refactoring

What if the price for each topping is different? 
Maybe "durian" topping costs more than "mushroom" topping.

There are two refactorings for this:

1. *Pass whole object instead of values* - instead of calling `size.price(len(toppings))`, use `size.price(toppings)`.
2. *Delegate to a Strategy* - pricing varies but sizes rarely change, so define a separate class to compute price.
   (Design principle: "*Separate the parts that vary from the parts that stay the same*")

## Reading

* Refactoring chapter in *Code Complete* 2nd Edition. Good overview but not much code.
* *Refactoring - Improving the Design of Existing Code* by Martin Fowler.  The bible on refactoring.  The first 4 chapters explain the fundamentals.
* https://refactoring.com. Online version of Fowler's book, very little detail.
* [Enumerations](https://docs.python.org/3/library/enum.html) in Python Library docs.

from typing import List, Callable, NoReturn, NamedTuple

from objects.location import Location


class Order:
    def __init__(self, location: Location, products: Dict[int, int]):
        self.location = location
        self.products = products

    def put(product: int, amount: int):
        if product not in self.products:
            raise "Unasked for product unload"
        elif self.products[product] < amount:
            raise "Too much delivered"
        self.products[product] -= amount


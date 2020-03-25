from typing import Dict

from objects.location import Location


class Order:
    def __init__(self, location: Location, products: Dict[int, int]):
        self.location = location
        self.products = products

    def put(self, product: int, amount: int):
        if product not in self.products:
            raise Exception("Unasked for product unload")
        elif self.products[product] < amount:
            raise Exception("Too much delivered")
        self.products[product] -= amount


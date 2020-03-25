from typing import Dict

from objects.location import Location


class Order:
    ID = 0

    def __init__(self, location: Location, products: Dict[int, int]):
        self.id = ID
        self.location = location
        self.products = products
        ID += 1

    def put(self, product: int, amount: int):
        if product not in self.products:
            raise Exception("Unasked for product unload")
        elif self.products[product] < amount:
            raise Exception("Too much delivered")
        self.products[product] -= amount


from typing import List, Callable, NoReturn, NamedTuple

from objects.location import Location


class Warehouse:
    ID = 0

    def __init__(self, loc: Location, stocks: List[int]):
        self.id = Warehouse.ID
        self.location = loc
        self.stocks = stocks
        Warehouse.ID += 1

    def get(self, product: int, amount: int):
        if self.stocks[product] < amount:
            raise Exception("Not enough stock")

        self.stocks[product] -= amount

    def put(self, product: int, amount: int):
        self.stock[product] += amount


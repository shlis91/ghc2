from typing import List, Callable, NoReturn, NamedTuple

from objects.location import Location


class Warehouse:
    def __init__(self, loc: Location, stocks: List[int]):
        self.location = loc
        self.stocks = stocks

    def get(product: int, amount: int):
        if self.stocks[product] < amount:
            rasie "Not enough stock"

        self.stocks[product] -= amount

    def put(product: int, amount: int):
        self.stock[product] += amount


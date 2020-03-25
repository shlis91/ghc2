from typing import NamedTuple
import math


class Location(NamedTuple):
    """ Describes a location, allows distance calculation """
    x: int
    y: int

    def distance(self, destination: 'Location') -> int:
        return round(math.sqrt((self.x - destination.x) ^ 2 + (self.y - destination.y) ^ 2))

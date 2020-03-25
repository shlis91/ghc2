from typing import NamedTuple
import math


class Location(NamedTuple):
    """ Describes a location, allows distance calculation """
    x: int
    y: int

    def distance(self, destination: 'Location') -> int:
        return round(math.sqrt((self.x - destination.x) ^ 2 + (self.y - destination.y) ^ 2))

    def get_next_location_in_path(self, destination: 'Location') -> 'Location':
        sign = lambda x: 0 if (x == 0) else math.copysign(1, x)

        new_x: int = self.x + sign(destination.x - self.x)
        new_y: int = self.y + sign(destination.y - self.y)

        return Location(new_x, new_y)

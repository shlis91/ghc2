from typing import NamedTuple
import math


class Location(NamedTuple):
    """ Describes a location, allows distance calculation """
    x: int
    y: int

    def distance(self, destination: 'Location') -> int:
        return round(math.sqrt((self.x - destination.x) ^ 2 + (self.y - destination.y) ^ 2))

    def get_next_location_in_path(self, destination: 'Location') -> 'Location':
        new_x: int = self.x + min(math.fabs(self.x - destination.x), 1)
        new_y: int = self.y + min(math.fabs(self.y - destination.y), 1)

        return Location(new_x, new_y)

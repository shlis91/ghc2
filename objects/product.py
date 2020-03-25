from typing import NamedTuple


class Product(NamedTuple):
    """ Describes a package object """
    package_id: int
    weight: int

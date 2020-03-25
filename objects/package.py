from typing import NamedTuple


class Package(NamedTuple):
    """ Describes a package object """
    package_id: int
    weight: int

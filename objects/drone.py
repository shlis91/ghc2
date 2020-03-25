from typing import Tuple, Callable, NoReturn

from objects.location import Location
from objects.package import Package


class Drone:

    def __init__(self, drone_id: int, location: Location):
        self.drone_id: int = drone_id
        self.location: Location = location

        self.latest_action: Tuple[Callable, bool] = (None, None)

    def _deliver(self, destination: Tuple[int, int], package: Package) -> NoReturn:
        """ Contains the logic for delivery,
        runs each turn while the drone is in delivery mode.

        :param destination: The delivery destination
        :param package: The package to be delivered
        """

    def deliver(self, destination: Tuple[int, int], package: Package, dry: bool = False) -> int:
        """ Commands the drone to deliver the package to the destination.

        :param destination: The delivery destination
        :param package: The package to be delivered
        :param dry: If True, the drone wont do the action,
        but the function will still return the duration.

        :return: The amount of turns required for the drone to deliver the package.
        """
        pass

    def turns_left(self) -> int:
        """ Amount of turns until the drone finishes his current action. """
        pass

    def do_turn(self):
        """ Need to be called every turn, causes the drone the do his current action """
        pass

from typing import Tuple, Callable, NoReturn, NamedTuple

from objects.location import Location
from objects.package import Package


class ActionTuple(NamedTuple):
    func: Callable
    args: tuple
    kwargs: dict


class Drone:
    def __init__(self, drone_id: int, location: Location):
        self.drone_id: int = drone_id
        self.location: Location = location

        self.current_action: ActionTuple = None

    def _deliver(self, destination: Location, package: Package) -> NoReturn:
        """ Contains the logic for delivery,
        runs each turn while the drone is in delivery mode.

        :param destination: The delivery destination
        :param package: The package to be delivered
        """
        pass

    def deliver(self, destination: Location, package: Package, dry: bool = False) -> int:
        """ Commands the drone to deliver the package to the destination.

        :param destination: The delivery destination
        :param package: The package to be delivered
        :param dry: If True, the drone wont do the action,
        but the function will still return the duration.

        :return: The amount of turns required for the drone to deliver the package.
        """
        if dry is False:
            self.current_action = ActionTuple(self._deliver, (destination, package), {})

        return self.location.distance(destination)

    def turns_left(self) -> int:
        """ Amount of turns until the drone finishes his current action. """
        pass

    def do_turn(self):
        """ Need to be called every turn, causes the drone the do his current action """
        pass

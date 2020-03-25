from typing import Callable, NoReturn, NamedTuple

from objects.location import Location
from objects.product import Product


class ActionTuple(NamedTuple):
    func: Callable
    destination: Location
    package: Product

    args: tuple = tuple()
    kwargs: dict = dict()


class Drone:
    def __init__(self, drone_id: int, location: Location):
        self.drone_id: int = drone_id
        self.location: Location = location

        self.current_action: ActionTuple = None

    @property
    def destination(self) -> Location:
        if self.current_action is not None:
            return self.current_action.destination

    def _deliver(self, product: Product) -> NoReturn:
        """ Contains the logic for delivery,
        runs each turn while the drone is in delivery mode.

        :param product: The package to be delivered
        """
        if self.location == self.destination:
            self.current_action = None
        else:
            self.location = self.location.get_next_location_in_path(self.destination)

    def _load(self, product: Product) -> NoReturn:
        """ Contains the logic for loading,
        runs each turn while the drone is in loading mode.

        :param product: The package to be loaded
        """
        if self.location == self.destination:
            self.current_action = None
        else:
            self.location = self.location.get_next_location_in_path(self.destination)

    def _unload(self, product: Product) -> NoReturn:
        """ Contains the logic for unloading,
        runs each turn while the drone is in unloading mode.

        :param product: The package to be unloaded
        """
        if self.location == self.destination:
            self.current_action = None
        else:
            self.location = self.location.get_next_location_in_path(self.destination)

    def _drone_action_logic(self, func: Callable, destination: Location, package: Product, dry: bool = False):
        """ Commands the drone to deliver the package to the destination.

        :param func: The function that will run while the drone is doing the action.
        :param destination: The delivery destination.
        :param package: The package to be delivered.
        :param dry: If True, the drone wont do the action,
            but the function will still return the duration.

        :return: The amount of turns required for the drone to complete the action.
        """
        if dry is False:
            self.current_action = ActionTuple(func, destination, package)

        return self.location.distance(destination)

    def deliver(self, destination: Location, package: Product, dry: bool = False) -> int:
        """ Commands the drone to deliver the package to the destination.
        Uses the '_drone_action_logic' to set the drone's goal and return duration.
        """
        return self._drone_action_logic(self._deliver, destination, package, dry)

    def load(self, destination: Location, package: Product, dry: bool = False) -> int:
        """ Commands the drone to load the package to the destination.
        Uses the '_drone_action_logic' to set the drone's goal and return duration.
        """
        return self._drone_action_logic(self._load, destination, package, dry)

    def unload(self, destination: Location, package: Product, dry: bool = False) -> int:
        """ Commands the drone to unload the package to the destination.
        Uses the '_drone_action_logic' to set the drone's goal and return duration.
        """
        return self._drone_action_logic(self._unload, destination, package, dry)

    def turns_left(self) -> int:
        """ Amount of turns until the drone finishes his current action. """
        return self.location.distance(self.current_action.destination) + 1

    def do_turn(self):
        """ Need to be called every turn,
        causes the drone the do his current action
        """
        action = self.current_action

        if action is not None:
            action.func(package=action.package, *action.args, **action.kwargs)

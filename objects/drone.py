from typing import Callable, NoReturn, NamedTuple, List
from functools import wraps

from objects.location import Location
from objects.order import Order
from objects.warehouse import Warehouse


class Task(NamedTuple):
    func: Callable
    destination: Location

    args: tuple = tuple()


class Drone:
    def __init__(self, drone_id: int, location: Location):
        self.drone_id: int = drone_id
        self.location: Location = location

        self.task_list: List[Task] = list()
        self.inventory: List[int] = list()

    @staticmethod
    def _requires_location(func):
        """ Runs before a drone action that requires the drone to be in a location.
        If the drone isn't yet in the location, it will move towards it without running the function.
        Else the function will run. """
        @wraps(func)
        def wrapper(self: Drone, order: Order) -> NoReturn:
            if self.location != order.location:
                self.location = self.location.get_next_location_in_path(self.destination)
            else:
                func(order)
        return wrapper

    @property
    def current_task(self) -> Task:
        if len(self.task_list) > 0:
            return self.task_list[0]

    @property
    def destination(self) -> Location:
        if self.current_task is not None:
            return self.current_task.destination

    @_requires_location
    def _deliver(self, order: Order):
        """ Contains the logic for delivery, runs each turn while the drone is in delivery mode. """
        for product_id in order.products:
            self.inventory.remove(product_id)

        self.task_list.pop()

    @_requires_location
    def _load(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Contains the logic for loading, runs each turn while the drone is in loading mode. """
        warehouse.get(product_id, amount)

        for _ in range(amount):
            self.inventory.append(product_id)

        self.task_list.pop()

    @_requires_location
    def _unload(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Contains the logic for unloading, runs each turn while the drone is in unloading mode. """
        for _ in range(amount):
            self.inventory.remove(product_id)

        warehouse.put(product_id, amount)

        self.task_list.pop()

    def deliver(self, order: Order):
        """ Order the drone to deliver an order """
        task: Task = Task(self._load, order.location, (order, ))

        self.task_list.append(task)

    def load(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Order the drone to load a certain amount of product """
        task: Task = Task(self._load, warehouse.location, (warehouse, product_id, amount))

        self.task_list.append(task)

    def unload(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Order the drone to unload a certain amount of product """
        task: Task = Task(self._unload, warehouse.location, (warehouse, product_id, amount))

        self.task_list.append(task)

    def turns_left(self) -> int:
        """ Amount of turns until the drone finishes his current action. """
        return self.location.distance(self.current_task.destination) + 1

    def do_turn(self):
        """ Need to be called every turn,
        causes the drone the do his current action
        """
        action = self.current_task

        if action is not None:
            action.func(*action.args)

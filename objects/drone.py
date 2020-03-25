from typing import Callable, NoReturn, NamedTuple, List
from functools import wraps

from objects.location import Location
from objects.order import Order
from objects.warehouse import Warehouse


class Task(NamedTuple):
    func: Callable
    destination: Location

    args: tuple = tuple()

    def name(self):
        return self.func.__name__.upper()[1]


def _requires_location(func):
    """ Runs before a drone task that requires the drone to be in a location.
    If the drone isn't yet in the location, it will move towards it without running the function.
    Else the function will run. """
    @wraps(func)
    def wrapper(self: "Drone", x, *args) -> NoReturn:
        self.turns += self.location.distance(self.destination)
        self.location = self.destination
        func(self, x, *args)
        self.finished_task_list.append(self.task_list.pop())

    return wrapper


class Drone:
    ID = 0

    def __init__(self, location: Location, product_weights, max_carry_weight):
        self.drone_id: int = Drone.ID
        self.location: Location = location

        self.turns = 0

        self.task_list: List[Task] = list()
        self.finished_task_list: List[Task] = list()

        self.inventory: List[int] = list()

        self.product_weights = product_weights
        self.max_carry_weight = max_carry_weight

        Drone.ID += 1

    @property
    def weight(self):
        weight: int = 0

        for product_id in self.inventory:
            weight += self.product_weights[product_id]

        return weight

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
            print(product_id, self.inventory)
            self.inventory.remove(product_id)

    @_requires_location
    def _load(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Contains the logic for loading, runs each turn while the drone is in loading mode. """
        warehouse.get(product_id, amount)
        print(product_id, "loading")

        for _ in range(amount):
            self.inventory.append(product_id)

    @_requires_location
    def _unload(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Contains the logic for unloading, runs each turn while the drone is in unloading mode. """
        for _ in range(amount):
            self.inventory.remove(product_id)

        warehouse.put(product_id, amount)

    def deliver(self, order: Order):
        """ Order the drone to deliver an order """
        task: Task = Task(self._deliver, order.location, (order, ))

        self.task_list.append(task)

    def load(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Order the drone to load a certain amount of product """

        if self.weight + self.product_weights[product_id] * amount > self.max_carry_weight:
            raise Exception("Drone will exceed max carry weight!")

        task: Task = Task(self._load, warehouse.location, (warehouse, product_id, amount))

        self.task_list.append(task)

    def unload(self, warehouse: Warehouse, product_id: int, amount: int):
        """ Order the drone to unload a certain amount of product """
        task: Task = Task(self._unload, warehouse.location, (warehouse, product_id, amount))

        self.task_list.append(task)

    def wait(self, duration):
        task: Task = Task(self._wait, self.destination, (duration,))

        self.task_list.append(task)

    def turns_left(self) -> int:
        """ Amount of turns until the drone finishes his current task. """
        return self.location.distance(self.current_task.destination) + 1

    def do_turn(self):
        """ Need to be called every turn,
        causes the drone the do his current task
        """
        task = self.current_task

        if task is not None:
            task.func(*task.args)

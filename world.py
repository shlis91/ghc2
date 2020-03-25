import itertools
import logging
from typing import List, Callable, NoReturn, NamedTuple

from objects.location import Location
from objects.warehouse import Warehouse
from objects.order import Order
from objects.drone import Drone


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('world')


class World:
    def __init__(self, file_name):
        self.warehouses = []
        self.orders = []
        self.products = []
        self.grid = Location(0, 0)
        self.turns = 0
        self.drones = []
        self.max_payload = 0
        self.time = 0
        self.parse_world(file_name)

    def step():
        self.time += 1

    def parse_world(self, file_name: str) -> NoReturn:
        with open(file_name, 'rb') as f:
            rows, cols, drone_count, turns, max_payload = [int(x) for x in f.readline().split()]
            self.grid = Location(rows, cols)
            self.drones = [Drone(Location(0,0)) for _ in range(drone_count)]
            self.turns = turns
            self.max_payload = max_payload

            product_types_count = int(f.readline())
            self.products = [int(x) for x in f.readline().split()]
            assert(len(self.products) == product_types_count)
        
            warehouse_count = int(f.readline())
            for wi in range(warehouse_count):
                row, col = [int(x) for x in f.readline().split()]
                stocks = [int(x) for x in f.readline().split()]
                self.warehouses.append(Warehouse(Location(row, col), stocks))

            order_count = int(f.readline())
            for ci in range(order_count):
                row, col = [int(x) for x in f.readline().split()]
                order_items_count = int(f.readline())
                items = [int(x) for x in f.readline().split()]
                cart = {}
                for item in items:
                    cart[item] = cart.setdefault(item, 0) 
                self.orders.append(Order(Location(row, col), cart))

        logger.info("World is of size %d X %d", rows, cols)
        logger.info("There are %d drones", drone_count)
        logger.info("There are %d turns", turns)
        logger.info("Maximum drone lift-off payload is: %d", max_payload)
        logger.info("There are %d drones", drone_count)
        logger.info("There are %d warehouses", warehouse_count)
        logger.info("There are %d orders", order_count)
        logger.debug(self.products)
        logger.debug(self.warehouses)
        logger.debug(self.orders)

    def write_results(self, file_name: str, drones: List[Drone]):
        with open(file_name, 'wb') as f: 
            for drone in drones:
                cmd = str(drone.drone_id)
                for task in drone.task_list:
                    name = task.name()
                    cmd += name
                    if name == "W":
                        cmd += task.args[0]
                    else:
                        facility_id = task.args[0].id
                        product = task.args[1]
                        amount = task.args[2]
                        cmd += str(facility_id) + str(product) + str(amount)
            f.write(cmd + "\n")

def main():
    world = World("dataset/busy_day.in")

if __name__ == '__main__':
    main()


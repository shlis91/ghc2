import itertools
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger('world')


class World:
    def __init__(self, file_name):
        self.warehouses = []
        self.orders = []
        self.products = []
        self.grid = (0, 0)
        self.turns = 0
        self.drones = 0
        self.max_payload = 0
        self.parse_world(file_name)

    def parse_world(self, file_name):
        with open(file_name, 'rb') as f:
            rows, cols, drone_count, turns, max_payload = [int(x) for x in f.readline().split()]
            self.grid = (rows, cols)
            self.drones = drone_count
            self.turns = turns
            self.max_payload = max_payload

            product_types_count = int(f.readline())
            self.products = [int(x) for x in f.readline().split()]
            assert(len(self.products) == product_types_count)
        
            warehouse_count = int(f.readline())
            for wi in range(warehouse_count):
                row, col = [int(x) for x in f.readline().split()]
                stocks = [int(x) for x in f.readline().split()]
                self.warehouses.append(((row, col), stocks))

            order_count = int(f.readline())
            for ci in range(order_count):
                row, col = [int(x) for x in f.readline().split()]
                order_items_count = int(f.readline())
                items = [int(x) for x in f.readline().split()]
                self.orders.append(((row, col), items))

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


def main():
    world = World("dataset/busy_day.in")

if __name__ == '__main__':
    main()


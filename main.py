from world import World
files = ['dataset/busy_day.in',
         'dataset/mother_of_all_warehouses.in',
         'dataset/redundancy.in']


def take_care_of_order(d, w, order):
    pl = 0
    # print("started")
    # print(order.products.items())
    for p in order.products.items():
        pid = p[0]
        pnum = p[1]
        pw = w.products[pid]
        if pl + pw > w.max_payload:
            # print("hihi")
            d.deliver(order)
        else:
            for wh in w.warehouses:
                if wh.stocks[pid] != 0:
                    load_amount = min(int((w.max_payload - pl) / pw), wh.stocks[pid], pnum)
                    print(load_amount)
                    d.load(wh, pid, load_amount)
                    pnum -= load_amount
                    pl -= load_amount * pw
                    if pnum == 0:
                        break
                    elif pl < pw:
                        # print("hi")
                        d.deliver(order)
                        pl = 0
    print(d.inventory)
    if len(d.inventory) > 0:
        # print("hihihi")
        d.deliver(order)

def strategy_0(f_src, f_dst):

    w = World(f_src)
    orders = w.orders
    drone_index = 0
    for order in w.orders:
        d = w.drones[drone_index]
        take_care_of_order(d, w, order)
        drone_index = (drone_index + 1) % len(w.drones)

    w.write_results(f_dst, w.drones)

strategy_0(files[0], 'outputs/busy_day.out')





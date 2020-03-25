from world import World
files = ['dataset/example.in',
         'dataset/busy_day.in',
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
            while (d.current_task is not None):
                d.do_turn()
        else:
            for wh in w.warehouses:
                if wh.stocks[pid] != 0:
                    load_amount = min(int((w.max_payload - pl) / pw), wh.stocks[pid], pnum)
                    d.load(wh, pid, load_amount)
                    while (d.current_task is not None):
                        d.do_turn()
                    pnum -= load_amount
                    pl += load_amount * pw
                    if pnum == 0:
                        break
                    elif pl < pw:
                        # print("hi")
                        d.deliver(order)
                        while (d.current_task is not None):
                            d.do_turn()
                        pl = 0
                print(d.inventory)
    if len(d.inventory) > 0:
        # print("hihihi")
        d.deliver(order)
        while (d.current_task is not None):
            d.do_turn()

def strategy_0(f_src, f_dst):

    w = World(f_src)
    orders = w.orders
    drone_index = 0
    for order in w.orders:
        d = w.drones[drone_index]
        take_care_of_order(d, w, order)
        print(d.task_list)
        drone_index = (drone_index + 1) % len(w.drones)
        break


    w.write_results(f_dst, w.drones)

strategy_0(files[1], 'outputs/busy_day.out')





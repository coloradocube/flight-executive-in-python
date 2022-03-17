from datasource import DataSource
import multiprocessing as mp
import time
from queue import Empty


def f1(name, q, shutdown_q):

    def getter(name):
        return name
    
    ds = DataSource(2, getter, [name])
    
    while shutdown_q.empty():
        ds.log()
        print(ds.poll())
        time.sleep(1/ds.frequency)
    
    # the data to return for the rockblock message
    # TODO: put actual timestamp
    msg = {'timestamp': ds.poll()}
    q.put(msg)

def f2(name, q, shutdown_q):
    
    def getter(name):
        return name
    
    ds = DataSource(3, getter, [name])
    
    while shutdown_q.empty():
        ds.log()
        print(ds.poll())
        time.sleep(1/ds.frequency)
    
    msg = {'timestamp': ds.poll()}
    q.put(msg)


def create_process(data_qs, shutdown_q, ps, f, name):
    
    # mp.Queue defaults: FIFO, infinite capacity
    q = mp.Queue()
    data_qs.append(q)
    
    p = mp.Process(target=f, args=(name, q, shutdown_q))
    p.start()
    ps.append(p)


def handle_processes():
    
    shutdown_q = mp.Queue()
    data_qs = []
    ps = []
    
    create_process(data_qs, shutdown_q, ps, f1, 'bob')
    create_process(data_qs, shutdown_q, ps, f2, 'caroline')
    
    
    time.sleep(2)
    shutdown_q.put(True)
    
    for p in ps:
        p.join()
    
    for q in data_qs:
        try:
            print(q.get_nowait())
        except Empty:
            print("Empty exception")
    
    shutdown_q.get()


if __name__ == '__main__':
    
    # default for Linux
    mp.set_start_method('spawn')
    
    p_handler_p = mp.Process(target=handle_processes)
    p_handler_p.start()
    
    print("stuff")
        
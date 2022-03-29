from datasource import DataSource
import multiprocessing as mp
import time
from datetime import datetime
from queue import Empty


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds')


def datasource_loop(ds, q, shutdown_q):
    while shutdown_q.empty():
        
        current_data = ds.poll()
        current_timestamp = get_timestamp()
        
        ds.log(current_timestamp, current_data)
        
        # Update the queue
        if not q.empty():
            q.get()
        msg = {current_timestamp: current_data}
        q.put(msg)
        
        time.sleep(1/ds.frequency)

def f1(name, q, shutdown_q):

    def getter(name):
        return [name, 'says', 'hi']
    
    ds = DataSource('./f1_log.csv', ['timestamp', 'name', 'msg1', 'msg2'], 2, getter, [name])
    
    datasource_loop(ds, q, shutdown_q)


def f2(name, q, shutdown_q):
    
    def getter(name):
        return [name, 'says', 'hi']
    
    ds = DataSource('./f2_log.csv', ['timestamp', 'name', 'msg1', 'msg2'], 3, getter, [name])
    
    datasource_loop(ds, q, shutdown_q)


def create_process(data_qs, shutdown_q, ps, f, name):
    
    # Defaults for mp.Queue: FIFO, infinite capacity
    q = mp.Queue()
    data_qs.append(q)
    
    p = mp.Process(target=f, args=(name, q, shutdown_q))
    p.start()
    ps.append(p)


def handle_processes():
    
    # The queue to trigger a shutdown
    shutdown_q = mp.Queue()
    
    # Queues that receive regularly updated data from each datasource
    data_qs = []
    
    # Each datasource runs in its own process
    ps = []
    
    create_process(data_qs, shutdown_q, ps, f1, 'bob')
    create_process(data_qs, shutdown_q, ps, f2, 'caroline')
    
    time.sleep(1)
    
    for q in data_qs:
        try:
            print(q.get_nowait())
        except Empty:
            print("Empty exception: queue is empty")
    
    time.sleep(1)
    
    for q in data_qs:
        try:
            print(q.get_nowait())
        except Empty:
            print("Empty exception: queue is empty")
    
    time.sleep(1)
    
    shutdown_q.put(True)
    
    for q in data_qs:
        try:
            print(q.get_nowait())
        except Empty:
            print("Empty exception: queue is empty")
    
    for p in ps:
        p.join()
    
    shutdown_q.get()


if __name__ == '__main__':
    
    # Default for Linux
    mp.set_start_method('spawn')
    
    p_handler_p = mp.Process(target=handle_processes)
    p_handler_p.start()
        
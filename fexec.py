import multiprocessing as mp
import time
from queue import Empty
import utils
from datasources import GNSS, TMP117
import serial
import io
import sys
import struct


def datasource_loop(ds, q, shutdown_q):
    
    start_time = time.time()
    while shutdown_q.empty():
        
        if time.time() - start_time > 1/ds.frequency:
            start_time = time.time()
            current_data = ds.poll()
            current_timestamp = utils.get_timestamp()
            
            ds.log(current_timestamp, current_data)
            
            # Update the queue
            #if not q.empty():
            #    q.get()
            msg = (ds.name, (current_timestamp,) + current_data)
            
            q.put(msg)
            
            # to reduce unnecessary battery usage
            time.sleep(0.01)

def tmp117(q, shutdown_q, name):
    
    header = ('timestamp', 'tmp117')
    freq = 2
    ds = TMP117(name, './tmp117_log.csv', header, freq)
    datasource_loop(ds, q, shutdown_q)


def gnss(q, shutdown_q, name):
    
    header = ('timestamp', 'lat', 'lon', 'alt')
    # 4.01 appears to be the optimal frequency to get the most
    # data from the GNSS receiver according to my experimentation
    freq = 4.01
    ds = GNSS(name, './gnss_log.csv', header, freq)
    
    datasource_loop(ds, q, shutdown_q)


def create_process(data_qs, shutdown_q, ps, f, name):
    
    # Defaults for mp.Queue: FIFO, infinite capacity
    q = mp.Queue()
    data_qs.append(q)
    
    p = mp.Process(target=f, args=(q, shutdown_q, name))
    p.start()
    ps.append(p)


def handle_processes():
    
    # The queue to trigger a shutdown
    shutdown_q = mp.Queue()
    
    # Queues that receive regularly updated data from each datasource
    data_qs = []
    
    # Each datasource runs in its own process
    ps = []
    
    create_process(data_qs, shutdown_q, ps, gnss, 'gnss')
    create_process(data_qs, shutdown_q, ps, tmp117, 'tmp117')
    
    loop_start_time = time.time()
    try:
        while time.time() - loop_start_time < 10:
            time.sleep(3)
            for q in data_qs:
                try:
                    print(q.get_nowait())
                except Empty:
                    print("Empty exception: queue is empty")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    shutdown_q.put(True)
    
    for p in ps:
        p.join()

    sensor_data = {}
    for q in data_qs:
        try:
            data = q.get_nowait()
            sensor_data[data[0]] = data[1]
            pass
        except Empty:
            print("Empty exception: queue is empty")
    
    shutdown_q.get()

    print()
    print(sensor_data)
    
    gnss_data = sensor_data['gnss']
    packed_gnss_data = GNSS.pack(gnss_data, GNSS.decimal_place_multiplier)
    print('packed gnss data: ', packed_gnss_data)
    print('packed gnss data size: ', struct.calcsize('3i'))
    unpacked_gnss_data = GNSS.unpack(packed_gnss_data, GNSS.decimal_place_multiplier)
    print('unpacked gnss data: ', unpacked_gnss_data)
    print('unpacked gnss data size: ', sys.getsizeof(unpacked_gnss_data))

if __name__ == '__main__':
    
    # Default for Linux
    mp.set_start_method('spawn')
    
    p_handler_p = mp.Process(target=handle_processes)
    p_handler_p.start()
        

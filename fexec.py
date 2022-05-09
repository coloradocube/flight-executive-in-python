import multiprocessing as mp
import time
from queue import Empty
import utils
import datasources
from datasources import GNSS, TMP117
import serial
import io
import sys
import struct
from adafruit_rockblock import RockBlock
import serial.tools.list_ports
import packing


def datasource_loop(ds, q, shutdown_q):
    """Calls log on the datasource and loads the queue; shuts down if needed
    
    ds - A datasource object
    q - The queue where the data will be loaded to be collected by the parent process
    shutdown_q - Empty until ready to shutdown
    """
    
    start_time = time.time()
    while shutdown_q.empty():
        
        if time.time() - start_time > 1/ds.frequency:
            start_time = time.time()
            current_data = ds.poll()
            current_timestamp = utils.get_timestamp()
            
            ds.log(current_timestamp, current_data)
            
            msg = (ds.name, (current_timestamp,) + current_data)
            
            q.put(msg)
            
            # to reduce unnecessary battery usage
            time.sleep(0.01)
        
    ds.close_file()


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


def create_sensor_process(data_qs, shutdown_q, ps, f, name):
    """Initializes each sensor's process along with its queue
    
    data_qs - The list of queues that will be used to transfer data from the datasource to the parent process
    shutdown_q - The queue that is used to gracefully shutdown the datasource loops
    ps - The list of processes to which this process will be added
    f - A callback function that initializes the datasource and begins the datasource loop
    """
    
    # Defaults for mp.Queue: FIFO, infinite capacity
    q = mp.Queue()
    data_qs.append(q)
    
    p = mp.Process(target=f, args=(q, shutdown_q, name))
    p.start()
    ps.append(p)


def init_rockblock():
    """Returns an adafruit rockblock object"""
    
    # Get correct port
    port = None
    for p in serial.tools.list_ports.comports():
        if p.product == 'TTL232R-3V3':
            port = p.device
    
    uart = serial.Serial(port, 19200)
    rb = RockBlock(uart)
    
    return rb


def rockblock_send(data_q, ready_q, shutdown_q):
    """Sends packed data from the RPi through the RockBLOCK; keep in mind this costs money and requires an open view of the clear sky
    
    data_q - A queue containing each packet of bytes ready to send through the RockBLOCK
    ready_q - This function fills the ready_q when it is ready to send
    shutdown_q - Allows this function to gracefully shutdown when the parent fills this queue
    """
    
    rb = init_rockblock()
    print("rb model: " + rb.model)
    
    while shutdown_q.empty():
            
        # Notify parent ready to send
        ready_q.put(True)
        
        rb.data_out = data_q.get()
        print("Talking to satellite...")
        retry = 0
        status = rb.satellite_transfer()
        
        print(status)
        while status[0] > 8:
            time.sleep(10)
            status = rb.satellite_transfer()
            print(retry, status)
            retry += 1
        print("\nRockBLOCK message sent.")


def handle_processes():
    """The parent of sensor and RockBLOCK processes; controls the flow of data between processes"""
    
    # The queue to trigger a shutdown
    shutdown_q = mp.Queue()
    
    # Queues that receive regularly updated data from each datasource
    data_qs = []
    
    # Each datasource runs in its own process
    ps = []
    
    create_sensor_process(data_qs, shutdown_q, ps, gnss, 'gnss')
    create_sensor_process(data_qs, shutdown_q, ps, tmp117, 'tmp117')
    
    # For the message to send through the RockBLOCK
    rb_data_q = mp.Queue()
    # Updated from the child when the RockBLOCK is ready to send
    rb_ready_q = mp.Queue()
    
    rb_p = mp.Process(target=rockblock_send, \
                      args=(rb_data_q, rb_ready_q, shutdown_q))
    rb_p.start()
    
    sensor_data = {}
    try:
        while True:
            # Wait between loops to save battery
            time.sleep(0.1)

            if not rb_ready_q.empty():
                
                rb_ready_q.get()
                
                # Collect the sensor data
                for q in data_qs:
                    try:
                        data = q.get()
                        print(data)
                        # data[0] is the name of the sensor
                        sensor_data[data[0]] = data[1]
                    except Empty:
                        print("Empty exception: queue is empty")
                
                print("sensor_data: {}".format(sensor_data))
                packed_msg = packing.pack_all(sensor_data)
                print("packed_msg: {}:".format(packed_msg))
                rb_data_q.put(packed_msg)
                #print(packing.unpack_all(packed_msg))
            
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    finally:
        shutdown_q.put(True)
        
        time.sleep(0.1)
        
        for p in ps:
            p.join()
        
        rb_p.join()
        
        shutdown_q.get()
    

if __name__ == '__main__':
    
    # Default for Linux
    mp.set_start_method('spawn')
    
    p_handler_p = mp.Process(target=handle_processes)
    p_handler_p.start()
        

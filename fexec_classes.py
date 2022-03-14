# TODO: add comments and documentation
# TODO: implement the code for the actual sensors
# TODO: test on the actual sensors


import time
from datetime import datetime
from collections import OrderedDict
import csv
import os
import serial
#from adafruit_rockblock import RockBlock


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds')


class TelemetryPoint:
    """A telemetry point with a header list and data list
   
   
   """
    
    def __init__(self, name, min_time_interval, data_getter, header, output_file_path='telemetry_logs', filename=None):
    
        self.name = name
        self.min_time_interval = min_time_interval
        self.data_getter = data_getter
        self.header = header
        self.output_file_path = output_file_path
        
        self.start_time = time.time()
        
        if filename == None:
            self.filename = os.path.join(self.output_file_path, self.name + '_log.csv')
        else:
            self.filename = os.path.join(self.output_file_path, self.filename)
        
        self.output_file = open(self.filename, 'a+', newline='')
        self.csv_writer = csv.writer(self.output_file)
        
        self.data = []
        
        # write the header
        if os.path.getsize(self.filename) == 0:
            self.csv_writer.writerow(['timestamp'] + header)
    
    def is_ready_to_update(self):
    
        if time.time() - self.start_time > self.min_time_interval:
            self.start_time = time.time()
            return True
        else:
            return False
    
    def update(self):
    
            self.data = self.data_getter()
    
    def log_to_csv(self):
        
        # when enough time has passed, update the message and log
        if self.is_ready_to_update():
            
            # call the telemetry point's data getter function to retrieve the latest input data
            self.update()
            
            # write data to file
            self.csv_writer.writerow([get_timestamp()] + self.data)
        
    def delete_all_file_data(self):
        self.output_file.truncate(0)
    
    def close_file(self):
        self.output_file.close()


class RockblockSender:
    
    def __init__(self, min_time_interval=10, max_messages=None, should_send=True):
        
        self.min_time_interval = min_time_interval
        self.max_messages = max_messages
        self.should_send = should_send
        
        self.start_time = time.time()
        
        #try:
        #    uart = serial.Serial("/dev/ttyUSB0", 19200)   # ttyUSBx has to be checked
        #except serial.serialutil.SerialException as e:
        #    print(e)
        
        #self.rb = RockBlock(uart)
        
        msg_count_filename = 'rockblock_msg_count.txt'
        self.msg_count_file = open(msg_count_filename, 'a+')
        
        self.msg_count = 0
        
        self.init_msg_count()
    
    def reset_msg_count(self):
        self.msg_count = 0
        self.msg_count_file.truncate(0)
        self.msg_count_file.write(str(self.msg_count))
    
    def init_msg_count(self):
        '''retrieves msg_count from a file in case of reboot'''
        self.msg_count_file.seek(0)
        
        content = self.msg_count_file.read()
        
        if content == '':
            self.msg_count_file.write(str(self.msg_count))
        else:
            self.msg_count = int(content)
            
    def increment_msg_count(self):
        
        self.msg_count += 1
        self.msg_count_file.truncate(0)
        self.msg_count_file.write(str(self.msg_count))
    
    def is_ready_to_send(self):
        
        max_exceeded = False
        
        if self.max_messages == None:
            max_exceeded = False
        else:
            max_exceeded = self.msg_count >= self.max_messages
        
        enough_time_passed = time.time() - self.start_time > self.min_time_interval
        
        if enough_time_passed and not max_exceeded:
            self.start_time = time.time()
            return True
        else:
            return False
    
    def send(self, msg):
        
        if self.should_send:
            #self.rb.data_out = str.encode(line)
            pass
        
        self.increment_msg_count()
        print(msg)
        return msg
    
    def close_file(self):
        self.msg_count_file.close()

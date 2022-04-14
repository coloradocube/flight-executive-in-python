import time
import csv
import os


class DataSource:
    
    decimal_place_multiplier = 1
    
    def __init__(self, name, file_path, header, frequency):
        
        """Creates a new DataSource object
       
       parameters:
       file_path: the output file path; of the form "file/path.csv"
       header: a list of strings that will be the first line of the csv file, e.g. ['timestamp', 'lat', 'lon']
       frequency: number of times the source should be polled per second
       getter_function: the function that polls the sensors for data; must return a list
       getter_args: a list of arguments to the getter function (optional)
       """
        
        self.name = name
        self.file_path = file_path
        self.header = header
        self.frequency = frequency
        
        self.data = []
        self.shutdown = False
        
        self.output_file = open(self.file_path, 'a+', newline='')
        self.csv_writer = csv.writer(self.output_file)
        
        if os.path.getsize(self.file_path) == 0:
            self.csv_writer.writerow(header)
        
    
    def poll(self):
        # Update the current data
        pass
    
    def log(self, timestamp, data):
        
        self.csv_writer.writerow((timestamp,) + data)
    
    def check(self):
        # for pre-flight check
        try:
            self.poll()
            return 0
        except:
            return -1
    
    @staticmethod
    def pack(format_, sensor_output, decimal_place_multiplier):
        
        packed_data = []
        for s in sensor_output:
            packed_data.append(round(s * decimal_place_multiplier))
        
        return struct.pack(format_, packed_data)
    
    @staticmethod
    def unpack(format_, packed_data, decimal_place_multiplier):
        
        unpacked = struct.unpack(format_, packed_data)
        unpacked_data = []
        for u in unpacked:
            unpacked_data.append(u / decimal_place_multiplier)
        
        return struct.unpack(format_, packed_data)



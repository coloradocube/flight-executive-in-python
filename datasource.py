import time
import csv
import os


class DataSource:
    
    def __init__(self, file_path, header, frequency, getter_function, getter_args=[]):
        
        """Creates a new DataSource object
       
       parameters:
       file_path: the output file path; of the form "file/path.csv"
       header: a list of strings that will be the first line of the csv file, e.g. ['timestamp', 'lat', 'lon']
       frequency: number of times the source should be polled per second
       getter_function: the function that polls the sensors for data; must return a list
       getter_args: a list of arguments to the getter function (optional)
       """
        
        self.file_path = file_path
        self.frequency = frequency
        self.getter_function = getter_function
        self.args = getter_args
        self.header = header
        
        self.data = []
        self.shutdown = False
        
        self.output_file = open(self.file_path, 'a+', newline='')
        self.csv_writer = csv.writer(self.output_file)
        
        if os.path.getsize(self.file_path) == 0:
            self.csv_writer.writerow(header)
        
    
    def poll(self):
        # Update the current data
        
        self.data = self.getter_function(*self.args)
        return self.data
    
    def log(self, timestamp, data):
        
        # For demo purposes
        print("log: {} {} {}".format(str(timestamp), str(self.frequency), str(data)))
        
        self.csv_writer.writerow([timestamp] + data)
        
    
    def get_current_time_stamp():
        # from GNSS receiver or system
        pass
    
    def check(self):
        # for pre-flight check
        try:
            self.poll()
            return 0
        except:
            return -1



if __name__ == '__main__':
    
    def f():
        print('hello')
    
    #args = ['hi', 'bye']
    ds = DataSource(1, f)
    
    ds.poll()
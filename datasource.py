import time


class DataSource:
    
    def __init__(self, frequency, getter_function, args=[], shutdown_q=None):
        
        """Creates a new DataSource object
       
       parameters:
       frequency - number of times the source should be polled per second
       getter_function - the function that polls for the data
       args - the arguments to the getter function (optional)
       """
        
        self.frequency = frequency
        self.getter_function = getter_function
        self.args = args
        self.shutdown_q = shutdown_q
        
        self.data = []
        self.shutdown = False
    
    def poll(self):
        # Update the current data
        
        self.data = self.getter_function(*self.args)
        return self.data
    
    def log(self):
        # to csv
        print(self.frequency, 'logging')
    
    def get_current_time_stamp():
        # from GNSS receiver or system
        pass
    
    def check(self):
        # for pre-flight check
        pass



if __name__ == '__main__':
    
    def f():
        print('hello')
    
    #args = ['hi', 'bye']
    ds = DataSource(1, f)
    
    ds.poll()
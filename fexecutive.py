import time
from datetime import datetime
from collections import OrderedDict

# Naming the headers to prevent typos
timestamp, acc, tmp, env = ('timestamp', 'acc', 'tmp', 'env')

last_rockblock_sent_time = time.time()
rockblock_interval_time = 4

start_times = {}

count = 0

names_list = [timestamp, acc, tmp, env]
rockblock_dict = OrderedDict(zip(names_list, ['' for _ in names_list]))

def log(name, min_time_interval, data_getter):
        
    if not name in start_times:
        start_times[name] = time.time()
        
    # when enough time has passed, log
    if time.time() - start_times[name] > min_time_interval:
        
        # reset the start time when a datum is logged
        start_times[name] = time.time()
        
        # retrieve the data
        data_to_log = data_getter()
        
        # update the dictionary with the most current data from this sensor
        rockblock_dict[name] = data_to_log
        
        # log IMU


# flight loop
while True:
    # The following values are not absolute, but my current guess
    # GNSS preferably < 0.1 seconds
    
    # reset the start time at the beginning of each iteration
    iteration_start_time = time.time()
    
    rockblock_dict['timestamp'] = datetime.now().isoformat(timespec='seconds')
    
    def get_acc_data():
        #time.sleep(1)
        return name + str(count)
    
    name = acc
    min_time_interval = 5
    log(name, min_time_interval, get_acc_data)
    
    def get_tmp_data():
        #time.sleep(1)
        return name + str(count)
    
    name = tmp
    min_time_interval = 5
    log(name, min_time_interval, get_tmp_data)
    
    def get_env_data():
        #time.sleep(3)
        return name + str(count)
    
    name = env
    min_time_interval = 8
    log(name, min_time_interval, get_env_data)
        
    
    rockblock_msg = ''
    
    if time.time() - last_rockblock_sent_time > rockblock_interval_time:
        rockblock_msg = ','.join([str(x) for x in rockblock_dict.values()])
        last_rockblock_sent_time = time.time()
        
        #send rockblock message
        print(rockblock_msg)
    
    count += 1
    
    time.sleep(0.1)
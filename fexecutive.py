import time
from datetime import datetime
from collections import OrderedDict


# naming the headers to prevent typos
timestamp, acc, tmp, env = ('timestamp', 'acc', 'tmp', 'env')

# used to send the rockblock message only after a minimum amount of time has passed
last_rockblock_sent_time = time.time()
rockblock_interval_time = 4

# used to only poll for data no sooner than when it makes sense to do so
# to prevent unnecessary overhead
start_times = {}

# for testing purposes
count = 0

# a dictionary to compile the rockblock message
names_list = [timestamp, acc, tmp, env]
rockblock_dict = OrderedDict(zip(names_list, ['' for _ in names_list]))


def log_to_csv(msg, filename):
    pass
        


def update_rockblock_msg_and_log(name, min_time_interval, data_getter):
        
    if not name in start_times:
        start_times[name] = time.time()
        
    # when enough time has passed, update the message and log
    if time.time() - start_times[name] > min_time_interval:
        
        # reset the start time when a datum is logged
        start_times[name] = time.time()
        
        # retrieve the data
        data_to_log = data_getter()
        
        # update the dictionary with the most current data from this sensor
        rockblock_dict[name] = data_to_log
        
        # append this data to its csv
        #log_to_csv(msg, filename)
        
        
def send_rockblock_msg():
    
    # to ensure that this static variable is used and updated globally
    global last_rockblock_sent_time
    
    rockblock_msg = ''
    
    if time.time() - last_rockblock_sent_time > rockblock_interval_time:
        rockblock_msg = ','.join([str(x) for x in rockblock_dict.values()])
        last_rockblock_sent_time = time.time()
        
        # send rockblock message
        print(rockblock_msg)


# flight loop
while True:

    # reset the start time at the beginning of each iteration
    iteration_start_time = time.time()
    
    rockblock_dict['timestamp'] = datetime.now().isoformat(timespec='seconds')
    
    def get_acc_data():
        #time.sleep(1)
        return acc + str(count)
    
    update_rockblock_msg_and_log(name=acc, min_time_interval=5, data_getter=get_acc_data)
    
    def get_tmp_data():
        #time.sleep(1)
        return tmp + str(count)
    
    update_rockblock_msg_and_log(name=tmp, min_time_interval=5, data_getter=get_tmp_data)
    
    def get_env_data():
        #time.sleep(3)
        return env + str(count)
    
    update_rockblock_msg_and_log(name=env, min_time_interval=8, data_getter=get_env_data)
    
    send_rockblock_msg()
    
    count += 1
    
    time.sleep(0.1)
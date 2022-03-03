# TODO: add comments and documentation
# TODO: create unit/integration tests
# TODO: implement the code for the actual sensors
# TODO: test on the actual sensors


import time
from datetime import datetime
from collections import OrderedDict
import csv


output_file_path = 'telemetry_logs'


class TelemetryPoint:

    global output_file_path
    
    def __init__(self, name, min_time_interval, data_getter):
    
        self.name = name
        self.min_time_interval = min_time_interval
        self.data_getter = data_getter
        
        self.start_time = time.time()
        
        filename = output_file_path + '/' + name + '_log.csv'
        self.output_file = open(filename, 'a', newline='')
        self.csv_writer = csv.writer(self.output_file)
        
        self.data = ''
        
        # write the header
        self.csv_writer.writerow(['timestamp', self.name])
    
    def is_ready_to_update(self):
    
        if time.time() - self.start_time > self.min_time_interval:
            self.start_time = time.time()
            return True
        else:
            return False
    
    def update(self):
    
            self.data = self.data_getter()
    
    def log_to_csv(self):
    
        self.csv_writer.writerow([get_timestamp(), self.data])
    
    def close_file(self):
        self.output_file.close()


class Rockblock:
    
    def __init__(self, min_time_interval=10, max_messages=None, should_send=True):
        
        self.min_time_interval = min_time_interval
        self.max_messages = max_messages
        self.should_send = should_send
        
        self.start_time = time.time()
        
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
            # send rockblock message
            pass
        else:
            print(msg)
        
        self.increment_msg_count()
    
    def close_file(self):
        self.msg_count_file.close()


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds')


def log(telemetry_point):
    
    # when enough time has passed, update the message and log
    if telemetry_point.is_ready_to_update():
        
        # call the telemetry point's data getter function to retrieve the latest input data
        telemetry_point.update()
        
        telemetry_point.log_to_csv()


# flight loop
def main_execution_loop(telemetry_points, rockblock):
    
    for point in telemetry_points:
        log(point)
    
    if rockblock.is_ready_to_send():
        rockblock_msg = ','.join([p.data for p in telemetry_points])
        rockblock.send(rockblock_msg)
    
    # for testing
    time.sleep(0.1)


def setup_telemetry_points():

    telemetry_points = []
        
    def get_acc_data():
        #time.sleep(1)
        return 'acc'
    
    acc = TelemetryPoint(name='acc', min_time_interval=2, data_getter=get_acc_data)
    telemetry_points.append(acc)
    
    def get_tmp_data():
        #time.sleep(1)
        return 'tmp'
    
    tmp = TelemetryPoint(name='tmp', min_time_interval=5, data_getter=get_tmp_data)
    telemetry_points.append(tmp)
    
    def get_env_data():
        #time.sleep(3)
        return 'env'
    
    env = TelemetryPoint(name='env', min_time_interval=8, data_getter=get_env_data)
    telemetry_points.append(env)
    
    return telemetry_points


def main():
    
    telemetry_points = setup_telemetry_points()
    rockblock = Rockblock(min_time_interval=4, should_send=False)
    
    rockblock.reset_msg_count()
    
    while True:
        # execute the flight loop
        # set send_rockblock_data to False for testing
        main_execution_loop(telemetry_points, rockblock)
    
    for point in telemetry_points:
        point.close_file()
    
    rockblock.close_file()


if __name__ == '__main__':
    main()
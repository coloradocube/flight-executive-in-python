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


class Rockblock:
    
    def __init__(self, min_time_interval=10):
        
        self.min_time_interval = min_time_interval
    
        self.start_time = time.time()
    
    def is_ready_to_send(self):
    
        if time.time() - self.start_time > self.min_time_interval:
            self.start_time = time.time()
            return True
        else:
            return False
    
    
    def send(self, msg):
        
        # send rockblock message
        print(msg)


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds')


# TODO put this function into the TelemetryPoint class?
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
    
    # For testing
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
    rockblock = Rockblock(min_time_interval=4)
    
    while True:
        main_execution_loop(telemetry_points, rockblock)


if __name__ == '__main__':
    main()
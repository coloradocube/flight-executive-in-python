import fexecutive as fe
import time
import math
import csv
        

def main():
    
    # setup telemetry points
    telemetry_points = []
        
    def get_acc_data():
        time.sleep(0.1)
        return 'acc'
    
    acc_min_time_interval = 0.1
    acc = fe.TelemetryPoint('acc', acc_min_time_interval, data_getter=get_acc_data, filename='test_acc_log.csv')
    acc.output_file.truncate(0)
    telemetry_points.append(acc)
    
    def get_tmp_data():
        time.sleep(0.1)
        return 'tmp'
    
    tmp_min_time_interval = 0.5
    tmp = fe.TelemetryPoint('tmp', tmp_min_time_interval, data_getter=get_tmp_data, filename='test_tmp_log.csv')
    tmp.output_file.truncate(0)
    telemetry_points.append(tmp)
    
    # run program
    rb_min_time_interval = 0.4
    max_messages = 5
    rockblock = fe.Rockblock(rb_min_time_interval, max_messages, should_send=False)
    
    rockblock.reset_msg_count()
    
    start_time = time.time()
    
    sent_messages = []
    
    time_to_test = rb_min_time_interval * max_messages + 1.5
    
    while time.time() - start_time <= time_to_test:
        # execute the flight loop
        # set send_rockblock_data to False for testing
        #fe.main_execution_loop(telemetry_points, rockblock)
        
        for point in telemetry_points:
            fe.log(point)
        
        if rockblock.is_ready_to_send():
            rockblock_msg = ','.join([p.data for p in telemetry_points])
            sent_messages.append(rockblock.send(rockblock_msg))
        
        # to prevent unnecessary iterations that drain the battery
        time.sleep(0.01)
        
    end_time = time.time()
    
    # run tests
    
    # test minimum time between messages
    if end_time - start_time >= rb_min_time_interval * max_messages:
        print("Success: At least the minimum time passed between messages")
    else:
        print("Failed: Not enough time passed between messages")
    
    # test number of rockblock messages sent
    rockblock.msg_count_file.seek(0)
    number_of_messages_in_file = int(rockblock.msg_count_file.read())
    number_of_messages_var = rockblock.msg_count
    number_of_messages_sent = len(sent_messages)
    
    if number_of_messages_in_file == number_of_messages_var and number_of_messages_var == number_of_messages_sent:
        print("Success: The number of rockblock messages sent is consistent")
    else:
        print("Failed: The number of rockblock messages sent is inconsistent")
    
    # test data logs
    acc.output_file.seek(0)
    tmp.output_file.seek(0)
    
    acc_lines = list(csv.reader(acc.output_file))
    tmp_lines = list(csv.reader(tmp.output_file))
    
    test_acc_lines = ['acc', 'acc', 'acc']
    test_tmp_lines = ['tmp', 'tmp', 'tmp']
    
    number_of_lines_to_test = 3
    
    if [line[1] for line in acc_lines][:number_of_lines_to_test] == test_acc_lines[:number_of_lines_to_test] and \
            [line[1] for line in tmp_lines][:number_of_lines_to_test] == test_tmp_lines[:number_of_lines_to_test]:
        print("Success: Data logging correctly")
    else:
        print("Failed: Data logging incorrectly")
    
    # close files
    for point in telemetry_points:
        point.close_file()
    
    rockblock.close_file()


if __name__ == '__main__':
    main()
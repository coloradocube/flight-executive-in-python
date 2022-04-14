from .datasource import DataSource
import io
import pynmea2
import serial
import time
import struct


class GNSS(DataSource):

    decimal_place_multiplier = 100000

    def __init__(self, name, file_path, header, frequency):
        super().__init__(name, file_path, header, frequency)
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=0.1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    
    def poll(self):
        '''Returns a tuple of long floats (lat, lon, alt)'''
        
        start_time = time.time()
        timeout_seconds = 1.5
        
        while time.time() - start_time < timeout_seconds:
            try:
                line = self.sio.readline()
                msg = pynmea2.parse(line)
                lat = None
                lon = None
                alt = None
                
                try:
                    lat = msg.latitude
                    lon = msg.longitude
                    alt = msg.altitude
                except AttributeError:
                    pass
                else:
                    return (lat, lon, alt)
            except serial.SerialException as e:
                print('Devise error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                #print('Parse error: {}'.format('could not parse'))
                continue
        return (-1.0, -1.0, -1.0)
    
    @staticmethod
    def pack(sensor_output, decimal_place_multiplier):
        lat = round(sensor_output[1] * decimal_place_multiplier)
        lon = round(sensor_output[2] * decimal_place_multiplier)
        alt = round(sensor_output[3] * decimal_place_multiplier)
        return struct.pack('3i', lat, lon, alt)
    
    @staticmethod
    def unpack(packed_data, decimal_place_multiplier):
        unpacked = struct.unpack('3i', packed_data)
        lat = unpacked[0] / decimal_place_multiplier
        lon = unpacked[1] / decimal_place_multiplier
        alt = unpacked[2] / decimal_place_multiplier
        return (lat, lon, alt)
            

if __name__ == '__main__':
    
    print(get_location())

    

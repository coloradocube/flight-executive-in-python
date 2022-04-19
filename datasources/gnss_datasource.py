from .datasource import DataSource
import io
import pynmea2
import serial
import time
import struct


class GNSS(DataSource):

    def __init__(self, name, file_path, header, frequency):
        super().__init__(name, file_path, header, frequency)
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    
    def poll(self):
        '''Returns a tuple of long floats (lat, lon, alt)'''
        
        start_time = time.time()
        timeout_seconds = 2.5
        
        while time.time() - start_time < timeout_seconds:
            try:
                line = self.sio.readline()
                msg = pynmea2.parse(line)
                lat = 361.0
                lon = 361.0
                # Double the lowest point on Earth (Dead Sea)
                alt = -830.0
                
                try:
                    lat = msg.latitude
                    lon = msg.longitude
                    if msg.altitude != None:
                        alt = msg.altitude
                except AttributeError:
                    pass
                else:
                    return (lat, lon, alt)
            except serial.SerialException as e:
                print('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                time.sleep(0.1)
            except UnicodeDecodeError as e:
                time.sleep(0.1)
        
        return (-1.0, -1.0, -1.0)

    

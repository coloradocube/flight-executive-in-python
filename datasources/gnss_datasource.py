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
        #ser = serial.Serial('/dev/serial1', 9600, timeout=0.1)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    
    def poll(self):
        '''Returns a tuple of long floats (lat, lon, alt)'''
        
        start_time = time.time()
        timeout_seconds = 2.5
        
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
                print('Device error: {}'.format(e))
                #time.sleep(0.1)
                break
            except pynmea2.ParseError as e:
                #print('Parse error: {}'.format('could not parse'))
                pass
        return (-1.0, -1.0, -1.0)

    

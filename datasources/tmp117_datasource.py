from .datasource import DataSource
import board
import adafruit_tmp117
import struct


class TMP117(DataSource):
    
    # For packing the temperature to 3 decimal places
    decimal_place_multiplier = 10**3
    
    def __init__(self, name, filepath, header, freq):
        super().__init__(name, filepath, header, freq)
        i2c = board.I2C()
        self.tmp117 = adafruit_tmp117.TMP117(i2c)
    
    def poll(self):
        return (self.tmp117.temperature,)
    
    @staticmethod
    def pack(sensor_output, decimal_place_multiplier):
        
        tmp = round(sensor_output[1] * decimal_place_multiplier)
        return struct.pack('h', tmp)
    
    @staticmethod
    def unpack(packed_data, decimal_place_multiplier):
        
        unpacked = struct.unpack('3i', packed_data)
        tmp = unpacked[1] / decimal_place_multiplier
        return (tmp)
    
    
from .datasource import DataSource
import board
import adafruit_tmp117
import struct


class TMP117(DataSource):
    
    def __init__(self, name, filepath, header, freq):
        super().__init__(name, filepath, header, freq)
        i2c = board.I2C()
        self.tmp117 = adafruit_tmp117.TMP117(i2c)
    
    def poll(self):
        return (self.tmp117.temperature,)
    
    
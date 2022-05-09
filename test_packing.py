import packing
import utils
import unittest
import struct


class TestPacking(unittest.TestCase):
    
    def setUp(self):
        
        self.timestamp1 = '2022-04-17T23:42:11.851'
        self.unpacked_ts1 = '23:42:11.851'
        
        self.timestamp2 = '2022-04-17T00:00:00.000'
        self.unpacked_ts2 = '0:0:0.0'
        
        self.timestamp3 = '2022-04-17T23:59:59.999'
        self.unpacked_ts3 = '23:59:59.999'
        
        self.ts_size = struct.calcsize(packing.ts_format)
        
        self.gnss_data = (
            self.timestamp1,
            123.45678912345678,
            456.78901234567891,
            7891.2)
        
        self.unpacked_gnss = (
            self.unpacked_ts1,
            123.45679,
            456.78901,
            7891.2)
        
        self.tmp117_data = (self.timestamp1, 24.6015625)
        self.unpacked_tmp117 = (self.unpacked_ts1, 24.602)
    
    def test_pack_unpack_timestamp(self):
        
        packed_ts1 = packing.pack_timestamp(self.timestamp1)
        unpacked_ts1 = packing.unpack_timestamp(packed_ts1)
        self.assertEqual(self.unpacked_ts1, unpacked_ts1)
        
        packed_ts2 = packing.pack_timestamp(self.timestamp2)
        unpacked_ts2 = packing.unpack_timestamp(packed_ts2)
        self.assertEqual(self.unpacked_ts2, unpacked_ts2)
        
        packed_ts3 = packing.pack_timestamp(self.timestamp3)
        unpacked_ts3 = packing.unpack_timestamp(packed_ts3)
        self.assertEqual(self.unpacked_ts3, unpacked_ts3)
        
    def test_timestamp_size(self):
        
        packed_ts = packing.pack_timestamp(self.timestamp1)
        ts_size = int(len(packed_ts.hex()) / 2)
        
        self.assertEqual(self.ts_size, ts_size)
        
    def test_pack_unpack_gnss(self):
        
        packed_gnss = packing.pack_gnss(self.gnss_data)
        unpacked_gnss = packing.unpack_gnss(packed_gnss)
        
        self.assertEqual(self.unpacked_gnss, unpacked_gnss)
    
    def test_gnss_size(self):
        
        pass
    
    def test_pack_unpack_tmp117(self):
        
        packed_tmp117 = packing.pack_tmp117(self.tmp117_data)
        unpacked_tmp117 = packing.unpack_tmp117(packed_tmp117)
        
        self.assertEqual(self.unpacked_tmp117, unpacked_tmp117)

    # TODO test_pack_all(), and other packing methods
    
    
    
        
        
        
        
        
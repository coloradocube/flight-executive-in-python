import utils
import struct
import unittest


class TestUtils(unittest.TestCase):
    
    def test_format_size(self):
        self.assertTrue(struct.calcsize(utils.format_) <= 4)
    
    def test_pack_and_unpack_timestamp(self):
        timestamp = utils.get_timestamp()
        packed_timestamp = utils.pack_timestamp(timestamp)
        unpacked_timestamp = utils.unpack_timestamp(packed_timestamp)

        self.assertEqual(timestamp.split('T')[1],
                         unpacked_timestamp)


if __name__ == '__main__':
    unittest.main()
    
    
    
import unittest
from datasources import TMP117


class TestTMP117(unittest.TestCase):
    
    def setUp(self):
        header = ('timestamp', 'tmp117')
        self.tmp117 = TMP117('tmp117', './tmp117_log.csv', header, freq=2)
    
    def test_poll(self):
        result = self.tmp117.poll()
        self.assertTrue(isinstance(result, tuple))
        self.assertTrue(isinstance(result[0], float))
    
    def tearDown(self):
        self.tmp117.close_file()


if __name__ == '__main__':
    unittest.main()
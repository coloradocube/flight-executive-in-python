from datasource import DataSource
from datetime import datetime
import time


def get_timestamp():
    return datetime.now().isoformat(timespec='seconds')


def getter(inp):
    return [inp]


ds = DataSource('test.csv', ['timestamp', 'header'], 4, getter, ['test'])

for _ in range(9):
    data = ds.poll()
    ds.log(get_timestamp(), data)
    time.sleep(1/ds.frequency)
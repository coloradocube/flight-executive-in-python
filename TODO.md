# TODO
- In packing.py, the methods pack_all(), get_combined_format(), and unpack_all() need to be able to generically accept any sensor data and ensure it all remains in the correct order. Right now, these methods are hardcoded, which could throw an exception and block if one of the sensor's data doesn't come in for any reason.
- In packing.py, the methods pack_all(), get_combined_format(), and unpack_all() need unit tests.
- Each datasource's port connections need to be customized based on the hardware setup.
- Directories should be created for tests and data to better organize the file structure.

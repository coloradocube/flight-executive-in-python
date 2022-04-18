import struct

# Keep 3 decimal places for millisecond precision
ts_sec_multiplier = 10**3
ts_format = '2BH'

gnss_multiplier = 10**5
gnss_format = '3i'

tmp117_multiplier = 10**3
tmp117_format = 'h'

def pack_timestamp(ts):
    
    time = ts.split('T')[1]
    split_time = time.split(':')
    hour = int(split_time[0])
    minute = int(split_time[1])
    second = int(round(float(split_time[2]) * ts_sec_multiplier))
    
    return struct.pack(ts_format, hour, minute, second)


def format_unpacked_timestamp(unpacked):
    
    hour = str(unpacked[0])
    minute = str(unpacked[1])
    second = str(unpacked[2] / ts_sec_multiplier)
    
    return ':'.join((hour, minute, second))


def unpack_timestamp(packed_ts):
    
    unpacked_ts = struct.unpack(ts_format, packed_ts)
    unpacked_ts = format_unpacked_timestamp(unpacked_ts)
    
    return unpacked_ts


def pack_gnss(sensor_data):
    
    packed_ts = pack_timestamp(sensor_data[0])
    lat = round(sensor_data[1] * gnss_multiplier)
    lon = round(sensor_data[2] * gnss_multiplier)
    alt = round(sensor_data[3] * gnss_multiplier)
    packed = packed_ts + struct.pack(gnss_format, lat, lon, alt)
    
    return packed


def unpack_gnss(packed_data):
    
    unpacked = struct.unpack(ts_format+gnss_format, packed_data)
    ts = format_unpacked_timestamp(unpacked)
    lat = unpacked[3] / gnss_multiplier
    lon = unpacked[4] / gnss_multiplier
    alt = unpacked[5] / gnss_multiplier
    
    return (ts, lat, lon, alt)


def pack_tmp117(sensor_data):
    
    packed_ts = pack_timestamp(sensor_data[0])
    tmp = round(sensor_data[1] * tmp117_multiplier)
    packed = packed_ts + struct.pack(tmp117_format, tmp)
    
    return packed


def unpack_tmp117(packed_data):
    
    unpacked = struct.unpack(ts_format+tmp117_format, packed_data)
    ts = format_unpacked_timestamp(unpacked)
    tmp = unpacked[3] / tmp117_multiplier
    
    return (ts, tmp)


def pack_all(sensor_data):
    
    packed = \
        pack_gnss(sensor_data['gnss']) + \
        pack_tmp117(sensor_data['tmp117'])
    
    return packed


def get_combined_format():
    print(struct.calcsize(ts_format + \
                          gnss_format + \
                          tmp117_format \
                          ))


def unpack_all(packed):
    
    unpacked = struct.unpack(get_combined_format(), packed)
    
    return unpacked
    






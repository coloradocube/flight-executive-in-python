


data_points = [tmp117.temperature, 
        bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude, 
        *icm.acceleration, *icm.gyro, *icm.magnetic, 
        ina.bus_voltage, ina.current, ina.power,
        psu_voltage, psu_capacity]


def setup_telemetry_points():

    telemetry_points = []
    
    def get_bme680():
        return [bme680.temperature, bme680.gas, bme680.relative_humidity, bme680.pressure, bme680.altitude]
    
    header = ['bme680_temp_in', 'bme680_gas', 'bme680_rel_hum', 'bme680_press', 'bme680_alt']
    bme680 = fe.TelemetryPoint(name='bme680', min_time_interval=1, data_getter=get_bme680, header=header)
    telemetry_points.append(icm_acc)
    
    def get_icm_acc():
        return icm.acceleration
    
    header = ['icm_acc_x', 'icm_acc_y', 'icm_acc_z']
    icm_acc = fe.TelemetryPoint(name='icm_acc', min_time_interval=1, data_getter=get_icm_acc, header=header)
    telemetry_points.append(icm_acc)
    
    def get_icm_gyro():
        return icm.gyro
    
    header = ['icm_gyro_x', 'icm_gyro_y', 'icm_gyro_z']
    icm_gyro = fe.TelemetryPoint(name='icm_gyro', min_time_interval=1, data_getter=get_icm_gyro, header=header)
    telemetry_points.append(icm_gyro)
    
    def get_icm_magn():
        return icm.magnetic
    
    header = ['icm_magn_x', 'icm_magn_y', 'icm_magn_z']
    icm_magn = fe.TelemetryPoint(name='icm_magn', min_time_interval=1, data_getter=get_icm_magn, header=header)
    telemetry_points.append(icm_magn)
    
    def get_ina():
        return [ina.bus_voltage, ina.current, ina.power]
    
    header = ['ina_bus_vol', 'ina_bus_cur', 'ina_bus_pow']
    ina = fe.TelemetryPoint(name='ina', min_time_interval=1, data_getter=get_ina, header=header)
    telemetry_points.append(icm_magn)
    
    def get_psu_voltage():
        bus = smbus.SMBus(1)
        address = I2C_ADDR
        read = bus.read_word_data(address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000 /16
        return voltage
    
    psu_vol = fe.TelemetryPoint(name='psu_vol', min_time_interval=1, data_getter=get_psu_vol, header=['psu_vol'])
    telemetry_points.append(psu_vol)
    
    def get_psu_capacity(bus):
        bus = smbus.SMBus(1)
        address = I2C_ADDR
        read = bus.read_word_data(address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped /256
        return capacity
    
    psu_cap = fe.TelemetryPoint(name='psu_cap', min_time_interval=1, data_getter=get_psu_cap, header=['psu_cap'])
    telemetry_points.append(psu_cap)
    
    def get_cpu_temp():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp = temp.replace("'C","")
        temp = temp.replace("\n","")
        return (temp.replace("temp=",""))
    
    cpu_temp = fe.TelemetryPoint(name='cpu_temp', min_time_interval=1, data_getter=get_cpu_temp, header=['cpu_temp'])
    telemetry_points.append(cpu_temp)
    

def main():
    
    telemetry_points = setup_telemetry_points()
    
    rockblock = fe.Rockblock(min_time_interval=10, should_send=True)


if __name__ == '__main__':
    main()
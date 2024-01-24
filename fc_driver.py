import socket
import time

from loguru import logger

from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer


def debug_fc(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read = client.write_register(address=0x3003, value=2,  slave=1)
            # read = client.write_register(address=0x3001, value=2, slave=1)
            # resp = client.read_holding_registers(address=0x3000, count=2, unit=1, slave=1)
            # print(resp.registers)
            # read = client.write_register(address=0x3000, value=40000, slave=1)
            # time.sleep(1)
            # resp = client.read_holding_registers(address=0x3000, count=1, unit=1, slave=1)
            print('ok')
            # print(resp.registers)
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def start_fc(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x3001, value=1, slave=1)
            if resp.isError():
                print('error during write parameter')
            else:
                print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def start_fc_rev(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x3001, value=2, slave=1)
            if resp.isError():
                print('error during write parameter')
            else:
                print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def stop_fc(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x3001, value=0x005, slave=1)
            if resp.isError():
                print('error during write parameter')
            else:
                print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_freq(ip_addr: str, freq):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # check freq range
            freq = int(float(freq) * 100)
            if not 0 <= freq <= 60000:
                print(f'value {freq/100} out of range 0-600')
                return
            resp = client.write_register(address=0x3000, value=freq, slave=1)

            if resp.isError():
                print('error during write parameter')
            else:
                print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_freq(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read actual motor speed
            resp = client.read_holding_registers(address=0x3000, count=1, unit=1, slave=1)
            if resp.isError():
                print('error during reading parameter')
            else:
                reference_motor_freq = int(resp.registers[0]) / 100
                print('ok')
                print(reference_motor_freq)
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_freq_realtime(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read actual motor speed
            resp = client.read_holding_registers(address=0xc02, count=1, unit=1, slave=1)
            if resp.isError():
                print('error during reading parameter')
            else:
                actual_motor_freq = int(resp.registers[0])/100
                print('ok')
                print(actual_motor_freq)
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_freq_limit_high(ip_addr: str, freq):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # check freq range
            freq = int(float(freq) * 100)
            if not 0 <= freq <= 60000:
                print(f'value {freq / 100} out of range 0-600')
                return
            resp1 = client.write_register(address=0x109, value=freq, slave=1)
            resp2 = client.write_register(address=0x10a, value=freq, slave=1)

            if not resp1.isError() and not resp2.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_freq_limit_high(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read max_freq
            resp1 = client.read_holding_registers(address=0x109, count=1, unit=1, slave=1)
            resp2 = client.read_holding_registers(address=0x10a, count=1, unit=1, slave=1)
            if not resp1.isError() and not resp2.isError():
                max_freq = int(resp1.registers[0]) / 100
                freq_limit_high = int(resp2.registers[0]) / 100
                print('ok')
                print(min(max_freq, freq_limit_high))
            else:
                print('error during reading parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_speed(ip_addr: str, speed):
    speed = int(speed)
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read factory motor speed
            resp1 = client.read_holding_registers(address=0x336, count=1, unit=1, slave=1)
            # read factory motor frequency
            resp2 = client.read_holding_registers(address=0x335, count=1, unit=1, slave=1)
            if not resp1.isError() and not resp2.isError():
                factory_motor_speed = int(resp1.registers[0])
                factory_motor_frequency = int(resp2.registers[0])/100
                # calculate max motor speed
                max_speed = int((600*factory_motor_speed)/factory_motor_frequency)
                # check for limit
                if not 0 <= speed <= max_speed:
                    print(f'value {speed} out of range 0-{max_speed}')
                    return
                # calculate target frequency
                target_frequency = (factory_motor_frequency / factory_motor_speed) * speed
                # write target frequency to bus
                resp3 = client.write_register(address=0x3000, value=int(target_frequency * 100), slave=1)
                if not resp3.isError():
                    print('ok')
                else:
                    print('error during write parameter')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_rpm(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read actual motor speed
            resp = client.read_holding_registers(address=0xc06, count=1, unit=1, slave=1)
            if not resp.isError():
                actual_motor_speed = int(resp.registers[0])
                print('ok')
                print(actual_motor_speed)
            else:
                print('error during reading parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_rpm_max(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read factory motor speed
            resp1 = client.read_holding_registers(address=0x336, count=1, unit=1, slave=1)

            # read factory motor frequency
            resp2 = client.read_holding_registers(address=0x335, count=1, unit=1, slave=1)

            # read max_freq
            resp3 = client.read_holding_registers(address=0x109, count=1, unit=1, slave=1)

            resp4 = client.read_holding_registers(address=0x10a, count=1, unit=1, slave=1)
            if not resp1.isError() and not resp2.isError() and not resp3.isError() and not resp4.isError():
                factory_motor_speed = int(resp1.registers[0])
                factory_motor_frequency = int(resp2.registers[0]) / 100
                max_freq = int(resp3.registers[0]) / 100
                limit_high = int(resp4.registers[0]) / 100
                freq_limit = min(max_freq, limit_high)
                # calculate max motor speed
                max_speed = int((freq_limit*factory_motor_speed)/factory_motor_frequency)
                print('ok')
                print(max_speed)
            else:
                print('error during reading parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_motor_data(ip_addr: str, voltage, current, power, frequency, speed):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp1 = client.write_register(address=0x337, value=int(voltage), slave=1)
            resp2 = client.write_register(address=0x338, value=int(float(current) * 10), slave=1)
            resp3 = client.write_register(address=0x334, value=int(float(power) / 100), slave=1)  # if power set in kW then use *10 if in W then /100
            resp4 = client.write_register(address=0x335, value=int(float(frequency) * 100), slave=1)
            resp5 = client.write_register(address=0x336, value=int(speed), slave=1)
            if not resp1.isError() and not resp2.isError() and not resp3.isError() and not resp4.isError() and not resp5.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_motor_data(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp1 = client.read_holding_registers(address=0x337, count=1, unit=1, slave=1)
            resp2 = client.read_holding_registers(address=0x338, count=1, unit=1, slave=1)
            resp3 = client.read_holding_registers(address=0x334, count=1, unit=1, slave=1)
            resp4 = client.read_holding_registers(address=0x335, count=1, unit=1, slave=1)
            resp5 = client.read_holding_registers(address=0x336, count=1, unit=1, slave=1)
            if not resp1.isError() and not resp2.isError() and not resp3.isError() and not resp4.isError() and not resp5.isError():
                print('ok')  # if power get in kW then use /10 if in W then *100
                print(
                    f'vac: {resp1.registers[0]}\naac: {resp2.registers[0] / 10}\nwac: {resp3.registers[0] * 100}\n'
                    f'hz: {resp4.registers[0] / 100}\nrpm: {resp5.registers[0]}')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_start_duration(ip_addr: str, duration):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x10d, value=int(float(duration) * 10), slave=1)
            if not resp.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_start_duration(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.read_holding_registers(address=0x10d, count=1, unit=1, slave=1)
            if not resp.isError():
                start_duration = resp.registers[0]
                print('ok')
                print(start_duration / 10)
            else:
                print('error during reading parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_stop_duration(ip_addr: str, duration: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x10e, value=int(float(duration) * 10), slave=1)
            if not resp.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_stop_duration(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.read_holding_registers(address=0x10e, count=1, unit=1, slave=1)
            if not resp.isError():
                stop_duration = resp.registers[0]
                print('ok')
                print(stop_duration / 10)
            else:
                print('error during reading parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_state(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()

    if success:
        resp = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        if not resp.isError():
            value = resp.registers[0]
            print('ok')
            # print(f'0b{value:08b}')

            if check_bit(value, 0):
                print('work')
            else:
                print('stop')

            if check_bit(value, 1):
                print('acc_on')
            else:
                print('acc_off')

            if check_bit(value, 2):
                print('dec_on')
            else:
                print('dec_off')

            if check_bit(value, 3):
                print('rev')
            else:
                print('fwd')

            if check_bit(value, 4):
                print('fault')
            else:
                print('normal')
        else:
            print('error during reading parameter')
    else:
        print('connection to FC failed')


def reset_to_default(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E64
            resp1 = client.write_register(address=0x140, value=1, slave=1)

            time.sleep(3)

            # write parameter E09
            resp2 = client.write_register(address=0x109, value=60000, slave=1)

            # write parameter E10
            resp3 = client.write_register(address=0x10a, value=60000, slave=1)

            # write parameter E11
            resp4 = client.write_register(address=0x10b, value=0, slave=1)
            if not resp1.isError() and not resp2.isError() and not resp3.isError() and not resp4.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def alarm_reset(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write 3001H
            resp = client.write_register(address=0x3001, value=0x7, slave=1)
            if not resp.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_alarm_code(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write 3001H
            resp = client.read_holding_registers(address=0x3003, count=1, unit=1, slave=1)
            if not resp.isError():
                print('ok')
                print(resp.registers[0])
            else:
                print('error during reading parameter')

        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def goto_rs485_mode(ip_addr):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E01
            resp1 = client.write_register(address=0x101, value=2, slave=1)
            # print('setting E01 to 2')

            # write parameter E02
            resp2 = client.write_register(address=0x102, value=6, slave=1)
            # print('setting E02 to 6')

            # write parameter E05
            resp3 = client.read_holding_registers(address=0x105, value=0x0, slave=1)
            # print('setting E05 to 0')
            if not resp1.isError() and not resp2.isError() and not resp3.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def goto_hands_mode(ip_addr):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E01
            resp1 = client.write_register(address=0x101, value=0, slave=1)
            # print('setting E01 to 0')
            # write parameter E02
            resp2 = client.write_register(address=0x102, value=1, slave=1)
            # print('setting E02 to 1')
            # write parameter E05
            resp3 = client.read_holding_registers(address=0x105, value=0x0, slave=1)
            # print('setting E05 to 0')
            if not resp1.isError() and not resp2.isError() and not resp3.isError():
                print('ok')
            else:
                print('error during write parameter')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def check_bit(value, bit):
    return value & 1 << bit != 0

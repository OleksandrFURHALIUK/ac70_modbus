import socket
import time

from loguru import logger

from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer


def debug_fc(ip_addr: str):
    logger.info(f'start fc cmd')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read = client.write_register(address=0x3003, value=2,  slave=1)
            # read = client.write_register(address=0x3001, value=2, slave=1)
            read = client.read_holding_registers(address=0x3003, count=1, unit=1, slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def start_fc(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # read = client.write_register(address=8193, value=18,  slave=1)
            resp = client.write_register(address=0x3001, value=2, slave=1)
            # read = client.read_holding_registers(address=0x3001, count=1, unit=1, slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def stop_fc(ip_addr: str):
    logger.info(f'stop fc cmd')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x3001, value=0x005, slave=1)
            # resp = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_frequency(ip_addr: str, frequency):
    logger.info('setting frequency')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x3000, value=int(float(frequency) * 100), slave=1)
            # read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
            print('ok')
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
            resp = client.write_register(address=0x336, value=int(speed), slave=1)
            factory_motor_speed = int(resp.registers[0])
            # read factory motor frequency
            resp = client.write_register(address=0x335, value=int(speed), slave=1)
            factory_motor_frequency = int(resp.registers[0])/100
            # calculate target frequency
            target_frequency = (factory_motor_frequency/factory_motor_speed)*speed
            # write target frequency to bus
            resp = client.write_register(address=0x3000, value=int(target_frequency * 100), slave=1)

            # resp = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def motor_init(ip_addr: str, voltage, current, power, frequency, speed):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x337, value=int(voltage), slave=1)
            resp = client.write_register(address=0x338, value=int(float(current) * 100), slave=1)
            resp = client.write_register(address=0x334, value=int(float(power) * 100), slave=1)
            resp = client.write_register(address=0x335, value=int(float(frequency) * 100), slave=1)
            resp = client.write_register(address=0x336, value=int(speed), slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def get_motor_data(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            voltage = client.read_holding_registers(address=0x337, count=1, unit=1, slave=1)
            current = client.read_holding_registers(address=0x338, count=1, unit=1, slave=1)
            power = client.read_holding_registers(address=0x334, count=1, unit=1, slave=1)
            frequency = client.read_holding_registers(address=0x335, count=1, unit=1, slave=1)
            speed = client.read_holding_registers(address=0x336, count=1, unit=1, slave=1)
            print(
                f'voltage: {voltage.registers[0]} V\ncurrent: {current.registers[0] / 100} A\npower: {power.registers[0] / 100} kW\n'
                f'frequency: {frequency.registers[0] / 100} Hz\nspeed: {speed.registers[0]} rpm')

            # todo add set_speed and get current speed
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_start_duration(ip_addr: str, duration):
    logger.info('set start duration')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x10d, value=int(float(duration) * 100), slave=1)
            print('ok')
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
            stop_duration = resp.registers[0]
            print(f'E-13 Deceleration time 1: {stop_duration / 100}')
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_stop_duration(ip_addr: str, duration: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            resp = client.write_register(address=0x10e, value=int(float(duration) * 100), slave=1)
            print('ok')
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
            stop_duration = resp.registers[0]
            print(f'E-14 Deceleration time 1: {stop_duration / 100}')
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def read_fc_state(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()

    if success:
        resp = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        value = resp.registers[0]

        print(f'0b{value:08b}')
    else:
        print('connection to FC failed')


def reset_to_default(ip_addr: str):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E64
            resp = client.write_register(address=0x140, value=1, slave=1)

            # write parameter E09
            resp = client.write_register(address=0x109, value=600 * 100, slave=1)

            # write parameter E10
            resp = client.write_register(address=0x10a, value=600 * 100, slave=1)

            # write parameter E11
            resp = client.write_register(address=0x10b, value=0, slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def switch_control_side_to_bus(ip_addr):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E01
            read = client.write_register(address=0x101, value=2, slave=1)
            print('setting E01 to 2')

            # write parameter E02
            resp = client.write_register(address=0x102, value=6, slave=1)
            print('setting E02 to 6')

            # write parameter E05
            resp = client.read_holding_registers(address=0x105, value=1, slave=1)
            print('setting E05 to 1')
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def switch_control_side_to_lcp(ip_addr):
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            # write parameter E01
            read = client.write_register(address=0x101, value=0, slave=1)
            print('setting E01 to 0')
            # write parameter E02
            resp = client.write_register(address=0x102, value=1, slave=1)
            print('setting E02 to 1')
            # write parameter E05
            resp = client.read_holding_registers(address=0x105, value=0, slave=1)
            print('setting E05 to 0')
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')

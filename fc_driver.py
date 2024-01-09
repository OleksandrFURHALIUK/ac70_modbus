import socket
import time

from loguru import logger

from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import ModbusRtuFramer


def start_fc(ip_addr: str):
    logger.info(f'start fc cmd')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=8193, value=18,  slave=1)
        # read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        print(read.registers)
    except Exception as e:
        logger.error(f'{str(e)}')


def stop_fc(ip_addr: str):
    logger.info(f'stop fc cmd')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=8193, value=0, slave=1)
        # read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        print(read.registers)
    except Exception as e:
        logger.error(f'{str(e)}')


def set_frequency(ip_addr: str, frequency: int):
    logger.info('setting frequency')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=8192, value=int(frequency*100),  slave=1)
        # read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        print(read.registers)
    except Exception as e:
        logger.error(f'{str(e)}')


def set_rpm(ip_addr: str, rpm: int):
    logger.info('setting rpm')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=8192, value=int(rpm), slave=1)
        # read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
        print(read.registers)
    except Exception as e:
        logger.error(f'{str(e)}')

def motor_init(ip_addr: str, voltage, current, power, frequency, rpm):
    logger.info('motor init')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=0x337, value=int(voltage), slave=1)
        read = client.write_register(address=0x338, value=int(float(current)*100), slave=1)
        read = client.write_register(address=0x334, value=int(float(power)*100), slave=1)
        read = client.write_register(address=0x335, value=int(float(frequency)*100), slave=1)
        read = client.write_register(address=0x336, value=int(rpm), slave=1)
        print('ok')
    except Exception as e:
        logger.error(f'{str(e)}')

def get_motor_data(ip_addr: str):
    logger.info('get motor data')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        voltage= client.read_holding_registers(address=0x337, count=1, unit=1, slave=1)
        current = client.read_holding_registers(address=0x338, count=1, unit=1, slave=1)
        power = client.read_holding_registers(address=0x334, count=1, unit=1, slave=1)
        frequency = client.read_holding_registers(address=0x335, count=1, unit=1, slave=1)
        rpm = client.read_holding_registers(address=0x336, count=1, unit=1, slave=1)
        print(f'voltage: {voltage.registers[0]},\ncurrent: {current.registers[0]/100},\npower: {power.registers[0]/100},\n'
              f'frequency: {frequency.registers[0]/100},\nrpm: {rpm.registers[0]}')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_start_duration(ip_addr:str, duration):
    logger.info('set start duration')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        read = client.write_register(address=8192, value=int(duration), slave=1)
        print('ok')
    except Exception as e:
        logger.error(f'{str(e)}')


def set_stop_duration(ip_addr:str, duration):
    logger.info('set start duration')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()
    try:
        if success:
            read = client.write_register(address=8192, value=int(duration), slave=1)
            print('ok')
        else:
            print('connection to FC failed')
    except Exception as e:
        logger.error(f'{str(e)}')


def read_fc_state(ip_addr: str):
    logger.info(f'read fc info')
    client = ModbusTcpClient(ip_addr, port=9761, framer=ModbusRtuFramer)
    success = client.connect()

    # read = client.read_holding_registers(address=3076, count=1, unit=1, slave=1)
    read = client.read_holding_registers(address=0x3002, count=1, unit=1, slave=1)
    print(read.registers)


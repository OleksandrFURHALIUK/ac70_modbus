import argparse
import sys

from loguru import logger

from fc_driver import start_fc, stop_fc, read_fc_state, set_frequency, set_rpm, motor_init, get_motor_data


def main():
    parser = argparse.ArgumentParser(description='AC70 frequency converter')
    parser.add_argument("IP", action='extend', nargs=1, type=str,

                        help='IP address to converter. For example 192.168.3.1')
    parser.add_argument('CMD', action='extend', nargs='+', type=str,
                        help='CMD')
    args = parser.parse_args()
    print(args)

    if 'start' in args.CMD:
        ip_addr = args.IP[0]
        start_fc(ip_addr=ip_addr)

    elif 'stop' in args.CMD:
        ip_addr = args.IP[0]
        stop_fc(ip_addr=ip_addr)

    elif 'read_state' in args.CMD:
        ip_addr = args.IP[0]
        read_fc_state(ip_addr=ip_addr)

    elif 'set_frequency' in args.CMD:
        ip_addr = args.IP[0]
        frequency = args.CMD[0]
        set_frequency(ip_addr=ip_addr, frequency=frequency)

    elif 'set_rpm' in args.CMD:
        ip_addr = args.IP[0]
        rpm = args.CMD[0]
        set_rpm(ip_addr=ip_addr, rpm=rpm)

    elif 'motor_init' in args.CMD:
        ip_addr = args.IP[0]
        voltage = args.CMD[1]

        current = args.CMD[2]
        power = args.CMD[3]
        frequency = args.CMD[4]
        rpm = args.CMD[5]
        motor_init(ip_addr=ip_addr, voltage=voltage, current=current, power=power, frequency=frequency, rpm=rpm)
    elif 'get_motor_data' in args.CMD:
        ip_addr = args.IP[0]
        get_motor_data(ip_addr=ip_addr)



if __name__ == '__main__':
    main()

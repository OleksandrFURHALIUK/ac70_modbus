import argparse
import sys

from loguru import logger

from fc_driver import start_fc, stop_fc, read_fc_state, set_frequency, set_speed, motor_init, get_motor_data, \
    set_start_duration, set_stop_duration, get_start_duration, get_stop_duration, reset_to_default, debug_fc, \
    switch_control_side_to_lcp, switch_control_side_to_bus, get_speed

commands = ['start', 'stop',
           'read_state',
           'set_frequency',
           'set_rpm', 'get_rpm',
           'motor_init', 'get_motor_data',
           'set_start_duration', 'get_start_duration',
           'set_stop_duration', 'get_stop_duration',
           'switch_control_side_to_lcp', 'switch_control_side_to_bus',
           'reset_to_default', 'alarm_reset', 'read_alarm_code'
           ]


def main():
    parser = argparse.ArgumentParser(prog='ac70',
                                     description='AC70 frequency converter tool',
                                     epilog='Basic cmd look like: ac70 192.168.3.198 read_state',
                                     usage='ac70 IP CMD [-CMD_ARGS]'
                                     )
    parser.add_argument("IP", action='extend', nargs=1, type=str, metavar='IP',
                        help='IP address ETH->RS485 converter. For example 192.168.3.198')
    parser.add_argument('CMD', action='extend', nargs=1, type=str, metavar='CMD', choices=commands,
                        help=f"Command from available list: {commands}")
    parser.add_argument('CMD_ARGS', action='extend', nargs='*', type=str, metavar='CMD_ARGS',
                        help='Command specific arguments')

    args = parser.parse_args()

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
        if not args.CMD_ARGS:
            print('missing frequency value')
            return
        frequency = args.CMD_ARGS[0]
        set_frequency(ip_addr=ip_addr, frequency=frequency)

    elif 'set_rpm' in args.CMD:
        ip_addr = args.IP[0]
        if not args.CMD_ARGS:
            print('missing rpm value')
            return
        speed = args.CMD_ARGS[0]
        set_speed(ip_addr=ip_addr, speed=speed)
    elif 'get_rpm' in args.CMD:
        ip_addr = args.IP[0]
        get_speed(ip_addr=ip_addr)

    elif 'motor_init' in args.CMD:
        if not args.CMD_ARGS:
            print('missing data for motor init')
            return
        try:
            ip_addr = args.IP[0]
            voltage = args.CMD_ARGS[0]
            current = args.CMD_ARGS[1]
            power = args.CMD_ARGS[2]
            frequency = args.CMD_ARGS[3]
            speed = args.CMD_ARGS[4]
        except Exception as e:
            print('not enough arguments')
            return
        motor_init(ip_addr=ip_addr, voltage=voltage, current=current, power=power, frequency=frequency, speed=speed)
    elif 'get_motor_data' in args.CMD:
        ip_addr = args.IP[0]
        get_motor_data(ip_addr=ip_addr)
    elif 'set_start_duration' in args.CMD:
        ip_addr = args.IP[0]
        if not args.CMD_ARGS:
            print('not enough arguments')
            return
        set_start_duration(ip_addr=ip_addr, duration=args.CMD_ARGS[0])
    elif 'get_start_duration' in args.CMD:
        ip_addr = args.IP[0]
        get_start_duration(ip_addr=ip_addr)
    elif 'set_stop_duration' in args.CMD:
        ip_addr = args.IP[0]
        if not args.CMD_ARGS:
            print('not enough arguments')
            return
        set_stop_duration(ip_addr=ip_addr, duration=args.CMD_ARGS[0])
    elif 'get_stop_duration' in args.CMD:
        ip_addr = args.IP[0]
        get_stop_duration(ip_addr=ip_addr)
    elif 'reset_to_default' in args.CMD:
        ip_addr = args.IP[0]
        reset_to_default(ip_addr=ip_addr)
    elif 'alarm_reset' in args.CMD:
        ip_addr = args.IP[0]
        alarm_reset(ip_addr=ip_addr)
    elif 'read_alarm_code' in args.CMD:
        ip_addr = args.IP[0]
        read_alarm_code(ip_addr=ip_addr)
    elif 'switch_control_side_to_lcp' in args.CMD:
        ip_addr = args.IP[0]
        switch_control_side_to_lcp(ip_addr=ip_addr)
    elif 'switch_control_side_to_bus' in args.CMD:
        ip_addr = args.IP[0]
        switch_control_side_to_bus(ip_addr=ip_addr)


    elif 'debug' in args.CMD:
        ip_addr = args.IP[0]
        debug_fc(ip_addr=ip_addr)


if __name__ == '__main__':
    main()

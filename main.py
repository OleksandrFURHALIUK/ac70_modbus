import argparse
import sys

from loguru import logger

from fc_driver import start_fc, stop_fc, get_state, set_freq, set_speed, set_motor_data, get_motor_data, \
    set_start_duration, set_stop_duration, get_start_duration, get_stop_duration, reset_to_default, debug_fc, \
    goto_hands_mode, goto_rs485_mode, get_rpm, alarm_reset, get_alarm_code, get_rpm_max, get_freq

commands = ['start', 'stop',
           'get_state',
           'set_freq', 'get_freq',
           'set_rpm', 'get_rpm', 'get_rpm_max',
           'set_motor_data', 'get_motor_data',
           'set_start_duration', 'get_start_duration',
           'set_stop_duration', 'get_stop_duration',
           'goto_hands_mode', 'goto_rs485_mode',
           'reset_to_default', 'alarm_reset', 'get_alarm_code',
            'debug'
           ]
epilog = """
This program is designed to control the frequency converter Veichi AC70 via rs485 network 
with Ethernet -> Rs485 converter VTR-E/485.\n

Basic cmd look like: ac70 192.168.3.198 read_state

"""

def main():
    parser = argparse.ArgumentParser(prog='ac70',
                                     description='AC70 frequency converter tool',
                                     epilog=epilog,
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

    elif 'get_state' in args.CMD:
        ip_addr = args.IP[0]
        get_state(ip_addr=ip_addr)

    elif 'set_freq' in args.CMD:
        ip_addr = args.IP[0]
        if not args.CMD_ARGS:
            print('missing frequency value')
            return
        freq = args.CMD_ARGS[0]
        set_freq(ip_addr=ip_addr, freq=freq)
    elif 'get_freq' in args.CMD:
        ip_addr = args.IP[0]
        get_freq(ip_addr=ip_addr)

    elif 'set_rpm' in args.CMD:
        ip_addr = args.IP[0]
        if not args.CMD_ARGS:
            print('missing rpm value')
            return
        speed = args.CMD_ARGS[0]
        set_speed(ip_addr=ip_addr, speed=speed)
    elif 'get_rpm' in args.CMD:
        ip_addr = args.IP[0]
        get_rpm(ip_addr=ip_addr)
    elif 'get_rpm_max' in args.CMD:
        ip_addr = args.IP[0]
        get_rpm_max(ip_addr=ip_addr)
    elif 'set_motor_data' in args.CMD:
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
        set_motor_data(ip_addr=ip_addr, voltage=voltage, current=current, power=power, frequency=frequency, speed=speed)
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
    elif 'get_alarm_code' in args.CMD:
        ip_addr = args.IP[0]
        get_alarm_code(ip_addr=ip_addr)
    elif 'goto_hands_mode' in args.CMD:
        ip_addr = args.IP[0]
        goto_hands_mode(ip_addr=ip_addr)
    elif 'goto_rs485_mode' in args.CMD:
        ip_addr = args.IP[0]
        goto_rs485_mode(ip_addr=ip_addr)

    elif 'debug' in args.CMD:
        ip_addr = args.IP[0]
        debug_fc(ip_addr=ip_addr)


if __name__ == '__main__':
    main()

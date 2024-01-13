import argparse
import sys

from loguru import logger

from fc_driver import start_fc, stop_fc, get_state, set_freq, set_speed, set_motor_data, get_motor_data, \
    set_start_duration, set_stop_duration, get_start_duration, get_stop_duration, reset_to_default, debug_fc, \
    goto_hands_mode, goto_rs485_mode, get_rpm, alarm_reset, get_alarm_code, get_rpm_max, get_freq, start_fc_rev

commands = ['start', 'start_rev', 'stop',
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
usage: ac70 IP CMD [-CMD_ARGS]

    This program is designed to control the frequency converter Veichi AC70 via rs485 network 
with Ethernet -> Rs485 converter VTR-E/485 with default port 9761\n 
Basic cmd look like: ac70 192.168.3.198 read_state

Possible cmd are:
        start - start motor forward direction
        
        start_rev - start motor reverse direction
        
        stop - stop motor
        
        set_freq 12.3 - set frequency, by writing value in to register with address 3000H.
                        during writing check input value in range 0-600 Hz 
                        
        get_freq - read register value with address C02H
        
        set_rpm 1550 - set target speed of drive as 1550 rpm. This use set_freq command to set target 
                    speed of drive. Target frequency calculating by next expression:
                    target_frequency = (factory_motor_frequency / factory_motor_speed) * speed
                    Input speed checked to be in range 0-rpm_max
        
        get_rpm - read current motor speed in rpm by reading register with address C06H
        
        get_rpm_max - calculated max motor speed by next expression max_speed = (600*factory_motor_speed)/factory_motor_frequency
         
        set_motor_data 220 10.3 2.2 50 2800 - set motor data:   Voltage 220 Volts, H55, 
                                                                Current 10.3 Ampere, H56, 
                                                                Power 2.2 kW, H52,
                                                                Frequency 50 Hz, H53,
                                                                Motor speed 2800 rpm, H54 
                                                            
        get_motor_data - return motor data reading registers H55, H56, H52, H53, H54
        
        set_start_duration 3.0 - set acceleration time 3 seconds by writing register with address 10DH
        
        get_start_duration - read register with address 10DH
        
        set_stop_duration 3.0 - set deceleration time 3 seconds by writing register with address 10EH
        
        get_stop_duration - read register with address 10EH
        
        goto_hands_mode - switch control side to local control panel. Write registers:  0 -> 101H
                                                                                        1 -> 102H
                                                                                        0 -> 105H
        goto_rs485_mode - switch control side to rs485 network. Write registers:    2 -> 101H
                                                                                    6 -> 102H
                                                                                    0 -> 105H
        get_state - read register with address 3002H. Represent as: running: work or stop
                                                                    acceleration: acc_on or acc_off 
                                                                    deceleration: dec_on or dec_off
                                                                    direction: fwd or rev
                                                                    error: fault or normal 
        alarm_reset - write value 0007H in to register 3001H
        
        get_alarm_code - read register with address 3003H. See fault code table.
        
        reset_to_default - write to parameter   E64 = 1
                                                E09 = 600
                                                E10 = 600
                                                E11 = 0
           
"""


def main():
    parser = argparse.ArgumentParser(prog='ac70',
                                     description='AC70 frequency converter tool',
                                     epilog=epilog,
                                     usage=argparse.SUPPRESS,
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     )
    parser.add_argument("IP", action='extend', nargs=1, type=str, metavar='IP',
                        help='IP address ETH->RS485 converter. For example 192.168.3.198')
    parser.add_argument('CMD', action='extend', nargs=1, type=str, metavar='CMD', choices=commands,
                        help=f"Command: {commands}")
    parser.add_argument('CMD_ARGS', action='extend', nargs='*', type=str, metavar='CMD_ARGS',
                        help='Command specific arguments')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if 'start' in args.CMD:
        ip_addr = args.IP[0]
        start_fc(ip_addr=ip_addr)

    if 'start_rev' in args.CMD:
        ip_addr = args.IP[0]
        start_fc_rev(ip_addr=ip_addr)

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

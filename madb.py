#!/usr/bin/env python3 -u

from android_utils import *


def main():
    if len(sys.argv) == 1:
        print(
            """usage:
            1. madb [command ...] (all command how adb)
            2. choice devices
            3. enter
            
            multiple connect device
            1. add to your env start with ADB_DEVICE, ex: ```ADB_DEVICE_XIAOMI = 192.168.1.100```
            2. madb connect
            3. choice devices
            4. enter""")
    elif len(sys.argv) == 2 and sys.argv[1] == "connect":
        adb_connect()
    elif sys.argv[1] in (
            'connect', 'devices', 'start-server', 'kill-server', 'help', 'version', '-s', '-a', '-d', '-t'):
        run_command(adb_command())
    else:
        for device in get_devices():
            run_command(adb_command(device))


if __name__ == '__main__':
    main()

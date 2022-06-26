#!/usr/bin/python3 -u

import inquirer
import subprocess
import argparse
import sys
import os


def get_devices():
    if sys.platform == "win32":
        devices = subprocess.check_output(
            """echo off && for /f "skip=1" %x in ('adb devices') do echo %x""", shell=True, text=True).splitlines()
    else:
        devices = subprocess.check_output("adb devices | egrep '\t(device|emulator)' | cut -f 1", shell=True,
                                          text=True).splitlines()
    select_devices = [
        inquirer.Checkbox('devices',
                          message="Pls select devices?",
                          choices=devices,
                          ),
    ]
    answers = inquirer.prompt(select_devices)
    target_devices = answers['devices']
    return target_devices


def adb_command(device=None):
    args_list = sys.argv[1:]
    args_str = " ".join(args_list)
    if device is None:
        return f"adb {args_str}"
    else:
        return f"adb -s {device} {args_str}"


def get_ip_from_env():
    env = os.environ.items()
    devices_ip = []

    for e, i in env:
        if e.startswith('ADB_DEVICE'):
            devices_ip.append(e + " = " + i)
    print("devices_ip", devices_ip)
    select_devices = [
        inquirer.Checkbox('devices',
                          message="Pls select devices?",
                          choices=devices_ip,
                          ),
    ]
    answers = inquirer.prompt(select_devices)
    target_devices = answers['devices']
    return target_devices


def adb_connect(ip):
    return f"adb connect {ip}"


def run_command(command):
    print(command)
    subprocess.run(command, shell=True, text=True)


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
        for d in get_ip_from_env():
            device, ip = d.split(" = ")
            run_command(adb_connect(ip))
    elif sys.argv[1] in (
            'connect', 'devices', 'start-server', 'kill-server', 'help', 'version', '-s', '-a', '-d', '-t'):
        run_command(adb_command())
    else:
        for device in get_devices():
            run_command(adb_command(device))


if __name__ == '__main__':
    main()

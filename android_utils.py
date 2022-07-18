#!/usr/bin/env python3 -u

import inquirer
import subprocess
import sys
import os
from wrapt_timeout_decorator import *


def get_devices_from_adb():
    if sys.platform == "win32":
        devices = subprocess.check_output(
            """echo off && for /f "skip=1" %x in ('adb devices') do echo %x""", shell=True, text=True).splitlines()
    else:
        devices = subprocess.check_output("adb devices | egrep '\t(device|emulator)' | cut -f 1", shell=True,
                                          text=True).splitlines()
    return devices


def get_devices():
    devices = get_devices_from_adb()

    if len(devices) == 0:
        print("\nNo connected devices\n")
        adb_connect()
        devices = get_devices_from_adb()

    if len(devices) == 0:
        sys.tracebacklimit = 0
        raise Exception(f"\33[31m\033[1m" + f"No active device for adb command")
    elif len(devices) > 1:
        select_devices = [
            inquirer.Checkbox('devices',
                              message="Pls select devices?",
                              choices=devices,
                              carousel=True,
                              ),
        ]
        answers = inquirer.prompt(select_devices)
        target_devices = answers['devices']
    elif len(devices) == 1:
        target_devices = [devices[0]]

    return target_devices


def adb_command(device=None):
    return gen_command("adb", device)


def scrcpy_command(device=None):
    return gen_command("scrcpy", device)


def gen_command(prefix=None, device=None):
    args_list = sys.argv[1:]
    args_str = " ".join(args_list)
    if device is None:
        return f"{prefix} {args_str}"
    else:
        return f"{prefix} -s {device} {args_str}"


def get_ip_from_env():
    env = os.environ.items()
    devices_ip = []

    for e, i in env:
        if e.startswith('ADB_DEVICE'):
            devices_ip.append(e + " = " + i)
    select_devices = [
        inquirer.Checkbox('devices',
                          message="Pls select devices?",
                          choices=devices_ip,
                          carousel=True,
                          ),
    ]
    answers = inquirer.prompt(select_devices)
    target_devices = answers['devices']
    return target_devices


def adb_connect_command(ip):
    return f"adb connect {ip}"


def adb_connect():
    second = 5
    for d in get_ip_from_env():
        device, ip = d.split(" = ")
        try:
            timeout(second)(run_command)((adb_connect_command(ip)))
        except TimeoutError:
            sys.tracebacklimit = 0
            raise Exception(f"\33[31m\033[1m" + f"Device with {ip} no connected on {second} seconds") from None


def run_command(command):
    print(command)
    subprocess.run(command, shell=True, text=True)

#!/usr/bin/python3 -u

import inquirer
import subprocess
import sys

def get_devices():
    devices = subprocess.check_output(
        "adb devices | egrep '\t(device|emulator)' | cut -f 1", shell=True, text=True).splitlines()
    select_devices = [
        inquirer.Checkbox('devices',
                          message="Pls select devices?",
                          choices=devices,
                          ),
    ]
    answers = inquirer.prompt(select_devices)
    target_devices = answers['devices']
    return target_devices


def adb_command(device = None):
    args_list = sys.argv[1:]
    args_str = " ".join(args_list)
    if device == None:
        return f"adb {args_str}"
    else:
        return f"adb -s {device} {args_str}"

def run_command(command):
        print(command)
        subprocess.run(command, shell=True, text=True)

def main():
    if sys.argv[1] in ('devices', 'start-server', 'kill-server', 'help', 'version', '-s', '-a', '-d', '-t'):
        run_command(adb_command())
    else:
        for device in get_devices():
            run_command(adb_command(device))


if __name__ == '__main__':
    main()

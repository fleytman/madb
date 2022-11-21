#!/usr/bin/env python3 -u

import inquirer
import subprocess
import sys
import os
import glob
from wrapt_timeout_decorator import *


def get_devices_from_adb():
    if sys.platform == "win32":
        devices = subprocess.check_output(
            """echo off && for /f "skip=1" %x in ('adb devices') do echo %x""", shell=True, text=True).splitlines()
    else:
        devices = subprocess.check_output("adb devices | egrep '\t(device|emulator)' | cut -f 1", shell=True,
                                          text=True).splitlines()
    return devices


def get_devices(with_connect=True):
    devices = get_devices_from_adb()

    if len(devices) == 0 and with_connect:
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
    return gen_args_command("adb", device)


def scrcpy_command(device=None):
    return gen_args_command("scrcpy", device)


def gen_command(prefix=None, device=None, postfix=None):
    if device is None:
        return f"{prefix} {postfix}"
    else:
        return f"{prefix} -s {device} {postfix}"


def gen_args_command(prefix=None, device=None):
    args_list = sys.argv[1:]
    args_str = " ".join(args_list)
    return gen_command(prefix, device, args_str)


def gen_install_command(packages, options, device=None):
    prefix = f"adb"
    command_list = []
    options_string = " ".join(options)
    for package in packages:
        command = f'install {options_string} "{package}"'
        command_list.append(gen_command(prefix, device, command))

    # final_command = ";  ".join(command_list)
    return command_list


def gen_install_multi_package_command(packages, options, device=None):
    prefix = f"adb"
    packages_string = " ".join(f'"{package}"' for package in packages)
    options_string = " ".join(options)
    command = f"install-multi-package {options_string} {packages_string}"
    return gen_command(prefix, device, command)


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


def select_packages(packages, default_packages=[]):
    package_paths = [
        inquirer.Checkbox('packages',
                          message="Pls select packages?",
                          choices=packages,
                          carousel=True,
                          default=default_packages,
                          ),
    ]
    answers = inquirer.prompt(package_paths)
    target_packages = answers['packages']
    return target_packages


def adb_connect_command(ip):
    return f"adb connect {ip}"


def adb_disconnect_command(ip):
    return f"adb disconnect {ip}"


def adb_connect():
    second = 5
    for d in get_ip_from_env():
        device, ip = d.split(" = ")
        try:
            timeout(second)(run_command)((adb_connect_command(ip)))
        except TimeoutError:
            print(f"\33[31m\033[1m" + f"Device with {ip} no connected on {second} seconds")


def adb_disconnect():
    second = 5
    for ip in get_devices(with_connect=False):
        try:
            timeout(second)(run_command)((adb_disconnect_command(ip)))
        except TimeoutError:
            print(f"\33[31m\033[1m" + f"Device with {ip} no disconnected on {second} seconds")


def adb_install():
    """Select apk from directories from multiple devices
    Support apk and apex
    Doesn't support aab, xapk and apks"""
    paths = []
    packages = []
    options = []

    for argv in sys.argv[2:]:
        if os.path.isdir(argv):
            paths.append(os.path.abspath(argv))
        elif os.path.isfile(argv) and argv.endswith((".apk", ".apex")):
            packages.append(os.path.abspath(argv))
        if argv.startswith(("-", "--")):
            options.append(argv)

    if len(paths + packages) == 0:
        paths = [os.getcwd()]

    default_packages = tuple(packages)
    for path in paths:
        packages += [os.path.abspath(item) for item in glob.glob(f"{path}/*.apk", recursive=True)]
        packages += [os.path.abspath(item) for item in glob.glob(f"{path}/*.apex", recursive=True)]

    # remove duplicates see https://stackoverflow.com/a/60518033/4121942
    packages = [*{*packages}]

    # TODO add character escaping
    if len(packages) == 1:
        for device in get_devices():
            run_command(adb_command(device))
    # TODO install all via adb install
    elif len(packages) > 1:
        selected_packages = select_packages(packages, default_packages)
        commands = []
        for device in get_devices():
            commands.append(gen_install_multi_package_command(selected_packages, options, device))

        # run in parallel
        processes = [subprocess.Popen(cmd, shell=True, text=True) for cmd in commands]
        # do other things here..
        # wait for completion
        for p in processes:
            print(p.args)
            p.wait()


def run_command(command):
    print(command)
    subprocess.run(command, shell=True, text=True)

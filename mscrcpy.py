#!/usr/bin/env python3 -u

from android_utils import *


def main():
    for device in get_devices():
        run_command(scrcpy_command(device))


if __name__ == '__main__':
    main()

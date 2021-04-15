import subprocess
import time

import keyboard


def reset():
    print("[WATCHDOG] RESET")
    subprocess.call("systemctl stop traspi", shell=True)
    time.sleep(0.5)
    subprocess.call("systemctl restart traspi", shell=True)


def stop():
    print("[WATCHDOG] STOP")
    subprocess.call("systemctl stop traspi", shell=True)


def main():

    keyboard.add_hotkey("f1", reset)
    keyboard.add_hotkey("f2", stop)

    while True:
        continue


main()

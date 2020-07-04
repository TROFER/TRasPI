import os
import subprocess
import psutil
import gpiozero

class Hardware:

    class CPU:

        def temperature():
            return round(gpiozero.CPUTemperature().temperature, 1)

        def load():
            return psutil.cpu_percent()

        def cur_speed():
            os.system("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq")
            return int(subprocess.check_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq", shell=True).decode())

        def max_speed():
            os.system("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq")
            return int(subprocess.check_output("cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq", shell=True).decode())

    class Memory:

        def load():
            return int(psutil.virtual_memory().used // 1000000)

        def vmem():
            return int(psutil.swap_memory().used // 1000000)
        
        def total():
            return int(psutil.virtual_memory().total // 1000000)



def constrain(n, start1, stop1, start2, stop2):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)
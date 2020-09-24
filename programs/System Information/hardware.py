import core
import os
import subprocess
from urllib import request

if core.sys.const.platform != "UNIX":
    core.log.debug("Loading Placeholder Functions due to Platform")
    def _base():
        return 0
    class Hardware:
        class CPU:
            temperature = load = cur_speed = max_speed = _base
        class Memory:
            load = vmem = total = _base

else: # == UNIX
    try:
        import psutil
        import gpiozero
    except ImportError:
        core.log.warning("Some dependancies could not be found")

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
            def load_percent():
                return int((psutil.virtual_memory().used // 1000000) / (psutil.virtual_memory().total // 1000000) * 100)
       
        class Network:
            def local_addr():
                os.system("hostname -I") 
                return subprocess.check_output("hostname -I", shell=True).decode()
            def public_addr():
                os.system("curl https://ipinfo.io/ip")
                return subprocess.check_output("curl https://ipinfo.io/ip", shell=True).decode()
            def internet_test():
                try:
                    request.urlopen("http://www.google.co.uk", timeout=2)
                    return True
                except BaseException as e:
                    print(e)
                    return False
            def ssh_login():
                try:
                    with open(f"{core.sys.const.path}user/ssh.txt", 'r') as pw:
                        return pw.read()
                except FileNotFoundError:
                    return "FNF Error"
        
        class Storage:
            def total():
                return round(psutil.disk_usage('/').total / 1000000000, 2)
            def used():
                return round(psutil.disk_usage('/').used / 1000000000, 2)
            def used_percent():
                return psutil.disk_usage('/').percent
            def free():
                return round(psutil.disk_usage('/').free / 1000000000, 2)

def constrain(n, start1, stop1, start2, stop2):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)

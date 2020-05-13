import os
import subprocess
import core
import cpu, memory, network, storage, hardware

try:
    import psutil
    import gpiozero
except ImportError:
    print("Warning: Some dependancies could not be found")

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.index = 0
        self.map = [cpu.main, memory.main, network.main, storage.main, hardware.main]
    
    async def show(self):
        if self._flag:
            self._flag = False
            res = await self.map[self.index]
            if res is None:
                self.finish()
            else:
                self.index = (self.index + res) % len(self.map)

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

        pass
    
    

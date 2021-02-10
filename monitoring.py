from subprocess import Popen
import psutil
import time

process = Popen(["python", "ais_cm.py"])
ps = psutil.Process(process.pid)

while process.poll() is None:
    print("Memory", ps.memory_percent())
    print("CPU", ps.cpu_percent())
    time.sleep(1)
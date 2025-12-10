from prometheus_client import start_http_server, Gauge
import psutil
import time

cpu_gauge = Gauge("smartdoctor_cpu_percent", "CPU usage percent")
mem_gauge = Gauge("smartdoctor_mem_percent", "Memory usage percent")
disk_gauge = Gauge("smartdoctor_disk_percent", "Disk usage percent")

start_http_server(5000, addr="0.0.0.0")
print("=== Exporter avviato sulla porta 5000 ===")

while True:
    cpu_gauge.set(psutil.cpu_percent())
    mem_gauge.set(psutil.virtual_memory().percent)
    disk_gauge.set(psutil.disk_usage('/').percent)
    time.sleep(5)

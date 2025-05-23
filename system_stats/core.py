# system_stats/core.py
import psutil, platform, socket, pyperclip
from cpuinfo import get_cpu_info
import GPUtil
from datetime import datetime

def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "os": f"{platform.system()} {platform.release()}",
        "cpu": get_cpu_info()['brand_raw'],
        "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())),
        "ram": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }

def get_cpu_usage():
    return psutil.cpu_percent(percpu=True)

def get_ram_stats():
    mem = psutil.virtual_memory()
    return {
        "used": round(mem.used / (1024**3), 2),
        "total": round(mem.total / (1024**3), 2),
        "percent": mem.percent
    }

def get_gpu_stats():
    gpus = GPUtil.getGPUs()
    return [{
        "name": gpu.name,
        "load": gpu.load * 100,
        "mem_total": gpu.memoryTotal,
        "mem_used": gpu.memoryUsed,
        "temp": gpu.temperature
    } for gpu in gpus]

def get_disk_stats():
    return [{
        "device": p.device,
        "mountpoint": p.mountpoint,
        "fstype": p.fstype,
        "usage": psutil.disk_usage(p.mountpoint)._asdict()
    } for p in psutil.disk_partitions()]

def get_ports():
    return [{
        "pid": c.pid,
        "laddr": f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "",
        "raddr": f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "",
        "status": c.status
    } for c in psutil.net_connections() if c.status != 'NONE']

def get_processes(limit=10):
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            procs.append(p.info)
        except psutil.NoSuchProcess:
            continue
    return sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:limit]

def get_temperatures():
    temps = psutil.sensors_temperatures()
    if not temps:
        return {"N/A": "Temperature data not available"}
    flat = {}
    for name, entries in temps.items():
        for entry in entries:
            flat[f"{name} {entry.label or entry.sensor}"] = entry.current
    return flat

def get_clipboard():
    try:
        return pyperclip.paste()
    except:
        return "Clipboard access failed"

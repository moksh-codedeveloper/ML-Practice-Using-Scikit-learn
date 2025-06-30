# data_collector.py
import psutil
import os
from datetime import datetime, timezone

def collect_metrics():
    try:
        process_count = len(psutil.pids())
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage('/')
        load1, load5, load15 = os.getloadavg()
        zombie_count = sum(
            1 for p in psutil.process_iter(['status']) 
            if p.info.get('status') == psutil.STATUS_ZOMBIE
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "process_count": process_count,
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "swap_percent": swap.percent,
            "disk_percent": disk.percent,
            "load_avg_1": load1,
            "load_avg_5": load5,
            "load_avg_15": load15,
            "zombie_count": zombie_count
        }

    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
if __name__ == "__main__":
    metrics = collect_metrics()
    print(metrics)
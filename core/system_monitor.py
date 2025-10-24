import time
import psutil
from datetime import datetime
from threading import Thread, Event
from config.logger import logger

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except Exception:
    GPU_AVAILABLE = False


class SystemMonitor:
    def __init__(self):
        self.stats_list = []
        self.stop_event = Event()
        self.thread = Thread(target=self._monitor_loop)

    def _monitor_loop(self):
        while not self.stop_event.is_set():
            self.stats_list.append({
                "timestamp": datetime.now().isoformat(),
                "cpu": self._get_cpu_info(),
                "memory": self._get_memory_info(),
                "gpu": self._get_gpu_info()
            })
            time.sleep(1)

    def _get_cpu_info(self):
        percent = psutil.cpu_percent(interval=0.5)
        per_core = psutil.cpu_percent(interval=0.5, percpu=True)
        logger.info(f"CPU Overall: {percent}%")
        return {"overall_percent": percent, "per_core_percent": per_core}

    def _get_memory_info(self):
        mem = psutil.virtual_memory()
        return {
            "total": round(mem.total / (1024 ** 3), 2),
            "available": round(mem.available / (1024 ** 3), 2),
            "used": round(mem.used / (1024 ** 3), 2),
            "percent": mem.percent
        }

    def _get_gpu_info(self):
        if not GPU_AVAILABLE:
            return None
        gpu_info_list = []
        for i in range(pynvml.nvmlDeviceGetCount()):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle).decode("utf-8")
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_info_list.append({
                "name": name,
                "memory_total": round(mem.total / (1024 ** 3), 2),
                "memory_used": round(mem.used / (1024 ** 3), 2),
                "utilization_gpu": util.gpu
            })
        return gpu_info_list

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()

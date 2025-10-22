import os
import platform
import psutil
import subprocess

def get_cpu_info():
    try:
        cpu_count = os.cpu_count()
        cpu_name = platform.processor()
        return {"cpu_name": cpu_name or "Unknown", "cpu_cores": cpu_count}
    except Exception as e:
        return {"error": f"CPU info not available: {e}"}

def get_ram_info():
    try:
        mem = psutil.virtual_memory()
        return {"total_ram_gb": round(mem.total / (1024 ** 3), 2)}
    except Exception as e:
        return {"error": f"RAM info not available: {e}"}

def get_storage_info():
    try:
        disk = psutil.disk_usage('/')
        return {
            "total_storage_gb": round(disk.total / (1024 ** 3), 2),
            "free_storage_gb": round(disk.free / (1024 ** 3), 2),
        }
    except Exception as e:
        return {"error": f"Storage info not available: {e}"}

def get_gpu_info():
    gpu_info = {"gpu_available": False, "gpu_name": None}

    # NVIDIA GPUs
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            gpu_info["gpu_available"] = True
            gpu_info["gpu_name"] = result.stdout.strip()
            return gpu_info
    except FileNotFoundError:
        pass

    # Apple Silicon GPU (MPS)
    try:
        import torch
        if torch.backends.mps.is_available():
            gpu_info["gpu_available"] = True
            gpu_info["gpu_name"] = "Apple MPS"
    except Exception:
        pass

    # CUDA GPU via PyTorch
    try:
        import torch
        if torch.cuda.is_available():
            gpu_info["gpu_available"] = True
            gpu_info["gpu_name"] = torch.cuda.get_device_name(0)
    except Exception:
        pass

    return gpu_info

def get_system_info():
    return {
        "os": platform.system(),
        "architecture": platform.machine(),
        **get_cpu_info(),
        **get_ram_info(),
        **get_storage_info(),
        **get_gpu_info(),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_info(), indent=2))

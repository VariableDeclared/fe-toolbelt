import os
import subprocess
import shutil
import platform
import psutil
from datetime import datetime

def get_cpu_info():
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    return cores, threads

def get_memory_info():
    mem = psutil.virtual_memory()
    total_gb = mem.total / (1024 ** 3)
    return total_gb

def get_memory_modules():
    if platform.system() == "Linux":
        try:
            output = subprocess.check_output(['sudo', 'dmidecode', '-t', 'memory'], text=True)
            modules = [line for line in output.split('\n') if "Size:" in line and "No Module Installed" not in line]
            return modules
        except Exception as e:
            return ["Could not retrieve memory module details: " + str(e)]
    return ["Memory module detection only supported on Linux with dmidecode."]

def get_disks(exclude_loop=True):
    disks = psutil.disk_partitions()
    disk_info = []
    for d in disks:
        if "loop" in d[0]:
            continue
        usage = psutil.disk_usage(d.mountpoint)
        disk_info.append(f"{d.device} ({d.mountpoint}) - {usage.total / (1024 ** 3):.2f} GB total")
    return disk_info

def ensure_stress_ng():
    if shutil.which("stress-ng") is None:
        print("stress-ng not found. Installing...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "stress-ng"], check=True)
            print("stress-ng installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install stress-ng. Please install it manually.")
            exit(1)
    else:
        print("stress-ng is already installed.")

def run_stress_ng(cores):
    print(f"Running stress-ng (10 seconds, {cores} CPU stressor)...")
    result = subprocess.run(["stress-ng", "--cpu", str(cores), "--timeout", "30m", "--metrics-brief"], capture_output=True, text=True)
    return result.stdout

def main():
    print("Gathering system information...")
    cores, threads = get_cpu_info()
    total_memory = get_memory_info()
    mem_modules = get_memory_modules()
    disks = get_disks()

    ensure_stress_ng()
    stress_result = run_stress_ng(cores=threads)

    print("\n--- System Report ---")
    print(f"Date: {datetime.now()}\n")
    print(f"CPU Cores: {cores}")
    print(f"Logical CPUs: {threads}")
    print(f"Total Memory: {total_memory:.2f} GB")
    print("Memory Modules:")
    for mod in mem_modules:
        print(f"  - {mod}")
    print("Connected Disks:")
    for disk in disks:
        print(f"  - {disk}")
    print("\n--- Stress Test Result ---")
    print(stress_result)

if __name__ == "__main__":
    main()

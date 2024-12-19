import GPUtil
import psutil
import time
import os
from datetime import datetime

log_file = "datalog.txt"

def list_processes():
    print(f"{'PID':<10} {'Name':<30} {'CPU (%)':<10} {'Memory (%)':<10}")
    print("-" * 60)
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            print(f"{proc.info['pid']:<10} {proc.info['name']:<30} {proc.info['cpu_percent']:<10.2f} {proc.info['memory_percent']:<10.2f}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def get_gpu_usage():
    try:
        gpus = GPUtil.getGPUs()
        gpu_stats = []
        for gpu in gpus:
            gpu_stats.append(
                f"GPU {gpu.id}: Utilization: {gpu.load * 100:.2f}% | VRAM: {gpu.memoryUsed:.2f}MB/{gpu.memoryTotal:.2f}MB"
            )
        return " | ".join(gpu_stats) if gpu_stats else "Intet grafikkort fundet."
    except Exception as e:
        return f"Fejl i at finde GPU stats: {e}"
    
def get_run_number(log_file):
    if not os.path.exists(log_file):
        return 1 
    with open(log_file, "r") as file:
        first_line = file.readline()
        if first_line.startswith("Run "):
            run_number = int(first_line.split()[1]) + 1
            return run_number
    return 1
    
def monitor_process(pid, log_file="datalog.txt"):
    try:
        proc = psutil.Process(pid)
        logical_cores = psutil.cpu_count(logical=True)  
        with open(log_file, "a") as file:
            while True:
                cpu_percent = proc.cpu_percent(interval=1)
                cpu_percent_scaled = (cpu_percent / logical_cores) * 100 
                cpu_percent_scaled = min(cpu_percent_scaled, 100) 
                ram_percent = proc.memory_percent()  
                thread_count = proc.num_threads() 
                gpu_usage = get_gpu_usage() 

                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                log_entry = (
                    f"{timestamp} | PID: {pid} | CPU: {cpu_percent_scaled:.2f}% | "
                    f"RAM: {ram_percent:.2f}% | Threads: {thread_count} | {gpu_usage}\n"
                )

                print(log_entry, end="")
                file.write(log_entry)

                time.sleep(2)  
                
    except psutil.NoSuchProcess:
        print(f"Process with PID {pid} no longer exists.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    try:
        while True:
            print("\nListing all running processes...\n")
            list_processes()

            pid = int(input("\nEnter the PID of the process you want to monitor (or 0 to refresh the list): "))
            if pid == 0:
                continue

            print(f"Monitoring process with PID: {pid}. Press Ctrl+C to stop.\n")
            monitor_process(pid, log_file)
            break

    except ValueError:
        print("Invalid PID. Please enter a valid number.")
    except KeyboardInterrupt:
        print("\nProgram exited.")

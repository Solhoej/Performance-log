import pandas as pd
import re

# File path (update with your file's location)
file_path = r"C:\Users\ElbekVejrup\Desktop\Programmering\Performance-log\Benchmarks Cyberpunk 2077 (Raster and raytracing).txt"

# Initialize variables
data = []
current_run = ""

# Regex to match benchmark lines and extract data
pattern = re.compile(
    r"CPU: ([\d.]+)% \| RAM: ([\d.]+)% \| Threads: (\d+) \| GPU 0: Utilization: ([\d.]+)% \| VRAM: ([\d.]+)MB/"
)

# Read the file line by line
with open(file_path, "r") as file:
    for line in file:
        # Detect the current benchmark run
        if "Run" in line:
            current_run = line.strip()
            continue
        
        # Match benchmark lines and extract relevant data
        match = pattern.search(line)
        if match:
            cpu, ram, threads, gpu_util, vram_used = match.groups()
            data.append({
                "Run": current_run,
                "CPU": float(cpu),
                "RAM": float(ram),
                "Threads": int(threads),
                "GPU Utilization": float(gpu_util),
                "VRAM Used (MB)": float(vram_used)
            })

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = "cyberpunk_benchmarks.xlsx"
df.to_excel(output_file, index=False)
print(f"Data has been saved to {output_file}")

from collections import Counter
from memory_profiler import memory_usage
import matplotlib.pyplot as plt
import string
import time
import os
import psutil
import gc

#GC FATTO
# - PRENDI IL RUN ID PER CREARE I PATH DINAMICI
# CERCA ANCORA IL TEMPO DI UTILIZZO DELLA CPU E 


def calculate_letter_frequency(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    # Count only alphabet letters (case-insensitive) 
    letter_counts = Counter(char.lower() for char in content if char.isalpha())

    with open('resources/performance_analysis/output_python/output.txt', 'w') as output_file:
        for letter in string.ascii_lowercase:
            frequency = letter_counts.get(letter, 0)
            output_file.write(f"{letter}: {frequency}\n")

run_id = 1 # DEFINED RUN ID HARD CODED
method = 1 #SAME

# Usage for 1 GB file
process1 = psutil.Process()
start_time1 = time.time()
gc_start_time1 = start_time1
gc.collect()
gc_end_time1 = time.time()
mem_usage_start1 = memory_usage()[0]
calculate_letter_frequency('resources/performance_analysis/input/1GB.txt')
mem_usage_end1 = memory_usage()[0]
max_memory_usage1 = process1.memory_info().peak_wset / (1024 ** 2)  # Convert to MB
timeExpired1 = time.time() - start_time1
gc_time_elapsed1 = (gc_end_time1 - gc_start_time1) * 1000
# print(f"GC time elapsed: {gc_time_elapsed1} ms")
# print(f"Maximum memory usage: {max_memory_usage1} MB")
# print(f"Execution time: {timeExpired1} seconds")

# # Usage for 100 MB file
process2 = psutil.Process()
start_time2 = time.time()
gc_start_time2 = start_time2
gc.collect()
gc_end_time2 = time.time()
mem_usage_start2 = memory_usage()[0]
calculate_letter_frequency('resources/performance_analysis/input/100MB.txt')
mem_usage_end2 = memory_usage()[0]
max_memory_usage2 = process2.memory_info().peak_wset / (1024 ** 2)  # Convert to MB
timeExpired2 = time.time() - start_time2
gc_time_elapsed2 = (gc_end_time2 - gc_start_time2) * 1000
# print(f"GC time elapsed: {gc_time_elapsed2} ms")
# print(f"Maximum memory usage: {max_memory_usage2} MB")
# print(f"Execution time: {timeExpired2} seconds")

# Usage for 1 MB file
process3 = psutil.Process()
start_time3 = time.time()
gc_start_time3 = start_time3
gc.collect()
gc_end_time3 = time.time()
mem_usage_start3 = memory_usage()[0]
calculate_letter_frequency('resources/performance_analysis/input/1MB.txt')
mem_usage_end3 = memory_usage()[0]
max_memory_usage3 = process3.memory_info().peak_wset / (1024 ** 2)  # Convert to MB
timeExpired3 = time.time() - start_time3
gc_time_elapsed3 = (gc_end_time3 - gc_start_time3) * 1000
# print(f"GC time elapsed: {gc_time_elapsed3} ms")
# print(f"Maximum memory usage: {max_memory_usage3} MB")
# print(f"Execution time: {timeExpired3} seconds")

# Usage for 10 KB file
process4 = psutil.Process()
start_time4 = time.time()
gc_start_time4 = start_time4
gc.collect()
gc_end_time4 = time.time()
mem_usage_start4 = memory_usage()[0]
calculate_letter_frequency('resources/performance_analysis/input/10KB.txt')
mem_usage_end4 = memory_usage()[0]
max_memory_usage4 = process4.memory_info().peak_wset / (1024 ** 2)  # Convert to MB
timeExpired4 = time.time() - start_time4
gc_time_elapsed4 = (gc_end_time4 - gc_start_time4) * 1000
# print(f"GC time elapsed: {gc_time_elapsed4} ms")
# print(f"Maximum memory usage: {max_memory_usage4} MB")
# print(f"Execution time: {timeExpired4} seconds")


# Usage for 1 GB file
with open('resources/performance_analysis/output_python/pyPerformances.txt', 'w') as file:
    file.write(f"GC time elapsed for 1 GB file: {gc_time_elapsed1} ms\n")
    file.write(f"Maximum memory usage for 1 GB file: {max_memory_usage1} MB\n")
    file.write(f"Execution time for 1 GB file: {timeExpired1} seconds\n\n")

# Usage for 100 MB file
with open('resources/performance_analysis/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 100 MB file: {gc_time_elapsed2} ms\n")
    file.write(f"Maximum memory usage for 100 MB file: {max_memory_usage2} MB\n")
    file.write(f"Execution time for 100 MB file: {timeExpired2} seconds\n\n")

# Usage for 1 MB file
with open('resources/performance_analysis/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 1 MB file: {gc_time_elapsed3} ms\n")
    file.write(f"Maximum memory usage for 1 MB file: {max_memory_usage3} MB\n")
    file.write(f"Execution time for 1 MB file: {timeExpired3} seconds\n\n")

# Usage for 10 KB file
with open('resources/performance_analysis/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 10 KB file: {gc_time_elapsed4} ms\n")
    file.write(f"Maximum memory usage for 10 KB file: {max_memory_usage4} MB\n")
    file.write(f"Execution time for 10 KB file: {timeExpired4} seconds\n\n")

print("performance analysis done, written to pyPerformances.txt")

# Values for the map reducer analysis, 1GB -> 100MB -> 1MB -> 10KB 
file_sizes = ['1 GB', '100 MB', '1 MB', '10 KB']
gc_times = [0,0,0,0]
memory_usages = [0,0,0,0]
execution_times = [0,0,0,0]

# GARBACE COLLECTOR
# ++++++++++++ SEARCHING BEST VALUEs ++++++++++++
map_gc_times = [] * 20
map_memory_usages = [] * 20
map_cpu_times = [] * 20

parameters_list = [
    "CPU time spent (ms)", 
    "GC time elapsed (ms)",
    "Peak Map Virtual memory (bytes)",
    "Execution time (s)" 
    ]
methods = ['combiner', 'inmappercombiner']
dim = ['10KB', '1MB', '100MB', '1GB']
n_reducers = 3

# in map vectors for each file size
for method in methods:
    for i in range(1, n_reducers+1):
        for dim_directory in os.listdir(f'resources/performance_analysis/output_{run_id}_{method}_{i}'):
            log_file = f'resources/performance_analysis/output_{run_id}_{method}_{i}/{dim_directory}/log.txt'
            with open(log_file, 'r') as f:
                for line in f:
                    if parameters_list[0] in line:
                        map_cpu_times.append(line.split("=")[1].strip())
                    elif parameters_list[1] in line:
                        map_gc_times.append(line.split("=")[1].strip())
                    elif parameters_list[2] in line:
                        map_memory_usages.append(line.split("=")[1].strip())
                        
            if dim_directory == '1GB':
                gc_times[0] = min(int(i) for i in map_gc_times)
                memory_usages[0] = min(int(i) for i in map_memory_usages)
                execution_times[0] = min(int(i) for i in map_cpu_times)
            elif dim_directory == '100MB':
                gc_times[1] = min(int(i) for i in map_gc_times)
                memory_usages[1] = min(int(i) for i in map_memory_usages)
                execution_times[1] = min(int(i) for i in map_cpu_times)
            elif dim_directory == '1MB':
                gc_times[2] = min(int(i) for i in map_gc_times)
                memory_usages[2] = min(int(i) for i in map_memory_usages)
                execution_times[2] = min(int(i) for i in map_cpu_times)
            elif dim_directory == '10KB':
                gc_times[3] = min(int(i) for i in map_gc_times)
                memory_usages[3] = min(int(i) for i in map_memory_usages)
                execution_times[3] = min(int(i) for i in map_cpu_times)

# Plotting the bar chart
x = range(len(file_sizes))
width = 0.10

fig, ax = plt.subplots()

#collect all local performances into arrays
pyCG = [gc_time_elapsed1,gc_time_elapsed2,gc_time_elapsed3,gc_time_elapsed4]
pyMem = [max_memory_usage1,max_memory_usage2,max_memory_usage3,max_memory_usage4]
pyExec = [timeExpired1,timeExpired2,timeExpired3,timeExpired4]

print("valori vettori python", pyCG, pyMem, pyExec)
print("valori vettori", gc_times, memory_usages, execution_times)


rects1 = ax.bar([i - width/2 for i in x], gc_times, width, label='GC Time')
rects2 = ax.bar([i + width/2 for i in x], memory_usages, width, label='Memory Usage')
rects3 = ax.bar([i + width/2 for i in x], execution_times, width, label='Execution Time')

pyRect1 = ax.bar([i - width/2 for i in x], pyCG, width, label='py GC Time')
pyRect2 = ax.bar([i - width/2 for i in x], pyMem, width, label='py Memory Usage')
pyRect3 = ax.bar([i - width/2 for i in x], pyExec, width, label='py Execution Time')

ax.set_ylabel('Values')
ax.set_title('Hadoop and Python Performance Analysis')
ax.set_xticks(x)
ax.set_xticklabels(file_sizes)
ax.legend()

all_values = gc_times + memory_usages + execution_times
ax.set_ylim([min(all_values) * 0.9, max(all_values) * 1.1]) 

# Set y-axis to logarithmic scale
ax.set_yscale('log')

fig.tight_layout()

plt.show()
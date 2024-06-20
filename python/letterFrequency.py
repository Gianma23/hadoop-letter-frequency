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
# print(f"Memory usage at start: {mem_usage_start1} MB")
# print(f"Memory usage at end: {mem_usage_end1} MB")
gc_time_elapsed1 = (gc_end_time1 - gc_start_time1) * 1000
print(f"GC time elapsed: {gc_time_elapsed1} ms")
print(f"Maximum memory usage: {max_memory_usage1} MB")
print(f"Execution time: {timeExpired1} seconds")

# Usage for 100 MB file
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
# print(f"Memory usage at start: {mem_usage_start2} MB")
# print(f"Memory usage at end: {mem_usage_end2} MB")
gc_time_elapsed2 = (gc_end_time2 - gc_start_time2) * 1000
print(f"GC time elapsed: {gc_time_elapsed2} ms")
print(f"Maximum memory usage: {max_memory_usage2} MB")
print(f"Execution time: {timeExpired2} seconds")

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
# print(f"Memory usage at start: {mem_usage_start3} MB")
# print(f"Memory usage at end: {mem_usage_end3} MB")
gc_time_elapsed3 = (gc_end_time3 - gc_start_time3) * 1000
print(f"GC time elapsed: {gc_time_elapsed3} ms")
print(f"Maximum memory usage: {max_memory_usage3} MB")
print(f"Execution time: {timeExpired3} seconds")

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
# print(f"Memory usage at start: {mem_usage_start4} MB")
# print(f"Memory usage at end: {mem_usage_end4} MB")
gc_time_elapsed4 = (gc_end_time4 - gc_start_time4) * 1000
print(f"GC time elapsed: {gc_time_elapsed4} ms")
print(f"Maximum memory usage: {max_memory_usage4} MB")
print(f"Execution time: {timeExpired4} seconds")


# Usage for 1 GB file
with open('resources/output_python/pyPerformances.txt', 'w') as file:
    file.write(f"GC time elapsed for 1 GB file: {gc_time_elapsed1} ms\n")
    file.write(f"Maximum memory usage for 1 GB file: {max_memory_usage1} MB\n")
    file.write(f"Execution time for 1 GB file: {timeExpired1} seconds\n\n")

# Usage for 100 MB file
with open('resources/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 100 MB file: {gc_time_elapsed2} ms\n")
    file.write(f"Maximum memory usage for 100 MB file: {max_memory_usage2} MB\n")
    file.write(f"Execution time for 100 MB file: {timeExpired2} seconds\n\n")

# Usage for 1 MB file
with open('resources/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 1 MB file: {gc_time_elapsed3} ms\n")
    file.write(f"Maximum memory usage for 1 MB file: {max_memory_usage3} MB\n")
    file.write(f"Execution time for 1 MB file: {timeExpired3} seconds\n\n")

# Usage for 10 KB file
with open('resources/output_python/pyPerformances.txt', 'a') as file:
    file.write(f"GC time elapsed for 10 KB file: {gc_time_elapsed4} ms\n")
    file.write(f"Maximum memory usage for 10 KB file: {max_memory_usage4} MB\n")
    file.write(f"Execution time for 10 KB file: {timeExpired4} seconds\n\n")


# Values for the map reducer analysis, 1GB -> 100MB -> 1MB -> 10KB 
file_sizes = ['1 GB', '100 MB', '1 MB', '10 KB']
gc_times = []
memory_usages = []
execution_times = []

# ++++++++++++ SEARCHING BEST VALUE FOR 1GB ++++++++++++
map_gc_times = []
with open('resources/performance_analysis/output_1_combiner_1/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[0] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_2/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[1] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_3/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[2] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_1/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[3] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_2/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[4] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_3/1GB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[5] = line.split('=')[1].strip()
gc_times[0] = min(map_gc_times)


# ++++++++++++ SEARCHING BEST VALUE FOR 100MB ++++++++++++
with open('resources/performance_analysis/output_1_combiner_1/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[0] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_2/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[1] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_3/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[2] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_1/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[3] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_2/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[4] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_3/100MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[5] = line.split('=')[1].strip()
gc_times[1] = min(map_gc_times)


# ++++++++++++ SEARCHING BEST VALUE FOR 1MB ++++++++++++
with open('resources/performance_analysis/output_1_combiner_1/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[0] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_2/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[1] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_3/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[2] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_1/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[3] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_2/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[4] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_3/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[5] = line.split('=')[1].strip()
gc_times[2] = min(map_gc_times)

# ++++++++++++ SEARCHING BEST VALUE FOR 10KB ++++++++++++
with open('resources/performance_analysis/output_1_combiner_1/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[0] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_2/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[1] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_combiner_3/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[2] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_1/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[3] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_2/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[4] = line.split('=')[1].strip()

with open('resources/performance_analysis/output_1_inmappercombiner_3/1MB/log.txt', 'r') as file:
    for line in file:
            if 'GC time elapsed (ms)' in line:
                # Split the line on the '=' sign and get the value, strip any whitespace
                map_gc_times[5] = line.split('=')[1].strip()
gc_times[3] = min(map_gc_times)

map_memory_usages = []  
map_execution_times = []  


# Plotting the bar chart
x = range(len(file_sizes))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, gc_times, width, label='GC Time')
rects2 = ax.bar(x + width/2, memory_usages, width, label='Memory Usage')
rects3 = ax.bar(x + width/2, execution_times, width, label='Execution Time')

ax.set_ylabel('Values')
ax.set_title('Letter Frequency Analysis')
ax.set_xticks(x)
ax.set_xticklabels(file_sizes)
ax.legend()

fig.tight_layout()

plt.show()
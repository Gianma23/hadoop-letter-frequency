from collections import Counter
import string
import time
import tracemalloc

def calculate_total_letter_count(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return len([char for char in content if char.isalpha()])

def calculate_letter_frequency(file_path, dim, total_letter_count):
    with open(file_path, 'r') as file:
        content = file.read()
    letter_counts = Counter(char.lower() for char in content if char.isalpha())
    with open(f'resources/python_performances/output_{dim}.txt', 'w') as output_file:
        for letter in string.ascii_lowercase:
            frequency = letter_counts.get(letter, 0)
            frequency = frequency / total_letter_count
            output_file.write(f"{letter}: {frequency}\n")
    return tracemalloc.take_snapshot()

def write_performances(parameter, dim, value, first_param=False, last_param=False):
    mode = 'a'
    if first_param:
        mode = 'w'
    with open(f'resources/python_performances/performances.txt', mode) as file:
        file.write(f'{parameter} for {dim} file: {value}\n')
        if last_param:
            file.write('\n')

def process_file(dim):
    input_file = f'resources/performance_analysis/input/{dim}.txt'
    start_time = time.process_time_ns()
    
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    total_letter_count = calculate_total_letter_count(input_file)
    snapshot_after = calculate_letter_frequency(input_file, dim, total_letter_count)
    
    memory_diff = snapshot_after.compare_to(snapshot_before, 'lineno')
    max_memory_usage = sum([stat.size_diff for stat in memory_diff])
    tracemalloc.stop()
    total_time = (time.process_time_ns() - start_time) * 1e-6 # convert to ms
    return max_memory_usage, total_time

run_id = 1
# file_dims = ['10KB', '1GB', '100MB', '1MB']
file_dims = ['1MB', '10KB']
first_param = True

for dim in file_dims:
    max_memory_usage, total_time = process_file(dim)
    write_performances('CPU time spent (ms)', dim, total_time, first_param)
    write_performances('Virtual memory (bytes) snapshot', dim, max_memory_usage, last_param=True)
    first_param = False
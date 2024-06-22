from collections import Counter
import string
import time

def calculate_total_letter_count(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return len([char for char in content if char.isalpha()])

def calculate_letter_frequency(file_path, dim, total_letter_count):
    with open(file_path, 'r') as file:
        content = file.read()
    letter_counts = Counter(char.lower() for char in content if char.isalpha())
    with open(f'../resources/python_performances/output_{dim}.txt', 'w') as output_file:
        for letter in string.ascii_lowercase:
            frequency = letter_counts.get(letter, 0)
            frequency = frequency / total_letter_count
            output_file.write(f"{letter}: {frequency}\n")

def process_file(dim):
    input_file = f'../resources/performance_analysis/input/{dim}.txt'
    start_time = time.process_time_ns()
    
    total_letter_count = calculate_total_letter_count(input_file)
    calculate_letter_frequency(input_file, dim, total_letter_count)
    
    total_time = (time.process_time_ns() - start_time) * 1e-6 # convert to ms
    return total_time
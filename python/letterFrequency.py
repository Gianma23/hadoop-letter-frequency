from collections import Counter
import string
import time
import os

def calculate_letter_frequency(file_path):

    with open(file_path, 'r') as file:
        content = file.read()

    # Count only alphabet letters (case-insensitive) 
    letter_counts = Counter(char.lower() for char in content if char.isalpha())

    with open('resources/performance_analysis/output_python/output.txt', 'w') as output_file:
        for letter in string.ascii_lowercase:
            frequency = letter_counts.get(letter, 0)
            output_file.write(f"{letter}: {frequency}\n")

# Example usage
start_time = time.time()
calculate_letter_frequency('resources/performance_analysis/input/1GB.txt')
print(f"Execution time: {time.time() - start_time} seconds")
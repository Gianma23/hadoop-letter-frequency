import pandas as pd
import matplotlib.pyplot as plt

dims = ['10KB', '1MB', '100MB', '1GB']
parameters_list = [
    'CPU time spent (ms)',
    'Virtual memory (bytes) snapshot'
]
run_id = 2

for params in parameters_list:
    df = pd.DataFrame(index=['Python', 'MapReduce'], columns=dims)
    df = df.fillna(0)
    py_file_path = 'resources/python_performances/performances.txt'
    with open(py_file_path, 'r') as file:
        for line in file:
            if params in line:
                line = line.split(':')
                for dim in dims:
                    if dim in line[0]:
                        df.loc['Python', dim] = float(line[1].strip())
    for dim in dims:
        mr_file_path = f'resources/performance_analysis/output_{run_id}_inmappercombiner_1/{dim}/log.txt'
        with open(mr_file_path, 'r') as file:
            for line in file:
                if params in line:
                    line = line.split('=')
                    df.loc['MapReduce', dim] += float(line[1].strip())
    if params == 'Virtual memory (bytes) snapshot':
        df = df / 1024
        parameters_list[1] = 'Virtual memory (KB) snapshot'
    print(df)
    ax = df.plot(kind='bar', figsize=(10, 5), title=params, rot=0)
    ax.set_yscale('log')
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom')
    plt.show()
    
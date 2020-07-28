import csv
import gc
import os
import time

import plotly.graph_objects as px
from memory_profiler import memory_usage
from plotly.subplots import make_subplots


def benchCode(benchFunc, *args):
    """
    Generalized code for benchmarking time and memory.

    Parameters
    ----------
    benchFunc : function
        Function to be benchmarked.

    Returns
    -------
    time1 : float
        Time benchmark of the function.

    mem1 : float
        Memory footprint of the function.
    """
    gc.disable()
    start = time.perf_counter()
    temp = [benchFunc(*args) for i in range(3)]
    time1 = (time.perf_counter() - start) / 3
    gc.enable()
    del temp

    mem1 = memory_usage((benchFunc, args))

    return time1, sum(mem1) / len(mem1)


def CSVWriter(path, func_dict, wall_time, mem_use):
    """
    Write the benchmark results to a CSV file.

    Parameters
    ----------
    path : string
        Path to the data folder for saving results.

    func_dict : dict
        Dictionary of all the functions to be saved.

    wall_time : list
        List of wall times for all functions.

    mem_use : list
        List of memory use for all functions.
    """
    for class_name, funcs in func_dict.items():
        for i, func_name in enumerate(funcs):
            if not os.path.isfile(f'{path}/{class_name}/{func_name}.csv'):
                os.makedirs(f'{path}/{class_name}', exist_ok=True)
                with open(f'{path}/{class_name}/{func_name}.csv',
                          'w+') as fptr:
                    writer = csv.writer(fptr)
                    writer.writerow([
                        'Commit_Tstamp', 'Commit_Msg', '100K', '1M', '10M',
                        '100M', '1B'
                    ])

        # PspecMain(bench_msg)

        # AvgCspecMain(bench_msg)
        # AvgPspecMain(bench_msg)
            with open(f'{path}/{class_name}/{func_name}.csv', 'a+') as fptr:
                writer = csv.writer(fptr)

                if func_name[0] == 'T':
                    writer.writerow(wall_time[int(i / 2)])

                elif func_name[0] == 'M':
                    writer.writerow(mem_use[int(i / 2)])


def CSVPlotter(path, class_name, func_name):
    """
    Plots results of benchmarks of a given function from a CSV file.

    Parameters
    ----------
    path : string
        Path to find files.

    class_name : string
        Name of the folder/class whose function is to be plotted.

    func_name : string
        Name of the file/function to be plotted.
    """
    flag = 0

    graph_val = ['100K', '1M', '10M', '100M', '1B']
    for root, dirs, files in os.walk(path):
        if root[root.rfind('/', 0, len(root)) + 1:len(root)] == class_name \
           and f'Time_{func_name}.csv' in files:
            flag = 1

            T_file = os.path.join(root, f'Time_{func_name}.csv')
            M_file = os.path.join(root, f'Mem_{func_name}.csv')

    if flag == 0:
        print("\nFunction does not exist. Run Benchmarks or Check the entered function name")
        exit(0)

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Execution Time(in s)(log)", "Memory Use(in MB)(log)"))

    with open(T_file, 'r+') as T_ptr:
        reader = csv.reader(T_ptr)

        for count, row in enumerate(reader):
            if count != 0 and row:
                fig.add_trace(px.Scatter(x=graph_val, y=row[2:], name=f'{row[0]}-{row[1]}'), row=1, col=1)
                fig.update_yaxes(type="log", row=1, col=1)

    with open(M_file, 'r+') as M_ptr:
        reader = csv.reader(M_ptr)

        for count, row in enumerate(reader):
            if count != 0 and row:
                fig.add_trace(px.Scatter(x=graph_val, y=row[2:], name=f'{row[0]}-{row[1]}'), row=1, col=2)
                fig.update_yaxes(type="log", row=1, col=2)

    fig.update_layout(title_text=f"Benchmark for {func_name}")
    fig.show()

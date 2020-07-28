
import time
import warnings
from datetime import datetime

import numpy as np

from stingray import AveragedPowerspectrum, Lightcurve
from utils import CSVWriter, benchCode

warnings.filterwarnings("ignore")


def createAvgPspec(lc, seg):
    AveragedPowerspectrum(lc, seg)


def AvgPspecMain(bench_msg):
    func_dict = {'AveragedPowerspectrum': ['Time_Init', 'Mem_Init']}

    wall_time = [[
        f'{datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")}',
        f'{bench_msg}',
    ] for i in range(int(sum([len(x) for x in func_dict.values()]) / 2))]
    mem_use = [[
        f'{datetime.utcfromtimestamp(int(time.time())).strftime("%Y-%m-%d %H:%M:%S")}',
        f'{bench_msg}',
    ] for i in range(int(sum([len(x) for x in func_dict.values()]) / 2))]

    for size in [10**i for i in range(5, 9)]:
        num_func = 0
        times = np.arange(size)
        counts = np.random.rand(size) * 100

        lc = Lightcurve(times, counts, dt=1.0, skip_checks=True)

        time1, mem1 = benchCode(createAvgPspec, lc, 10000)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        del lc, times, counts, time1, mem1

    CSVWriter(func_dict, wall_time, mem_use)
    del func_dict, wall_time, mem_use

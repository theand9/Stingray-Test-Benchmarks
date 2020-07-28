import time
import warnings
from datetime import datetime

import numpy as np

from stingray import AveragedCrossspectrum, Lightcurve
from utils import CSVWriter, benchCode

warnings.filterwarnings("ignore")


def createAvgCspec(lc1, lc2, seg):
    AveragedCrossspectrum(lc1, lc2, seg, silent=True)


def coherAvgCspec(avg_Cspec):
    avg_Cspec.coherence()


def TlagAvgCspec(avg_Cspec):
    avg_Cspec.time_lag()


def AvgCspecMain(bench_msg):
    func_dict = {
        'AveragedCrossspectrum': [
            'Time_Init', 'Mem_Init', 'Time_Coher', 'Mem_Coher', 'Time_Tlag',
            'Mem_Tlag'
        ],
    }

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
        lc_other = Lightcurve(times,
                              counts * np.random.rand(size),
                              dt=1.0,
                              skip_checks=True)

        time1, mem1 = benchCode(createAvgCspec, lc, lc_other, 10000)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        avg_cspec = AveragedCrossspectrum(lc, lc_other, 10000, silent=True)

        time1, mem1 = benchCode(coherAvgCspec, avg_cspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(TlagAvgCspec, avg_cspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        del avg_cspec, lc, lc_other, times, counts, time1, mem1

    CSVWriter(func_dict, wall_time, mem_use)
    del func_dict, wall_time, mem_use

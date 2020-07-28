import time
import warnings
from datetime import datetime

import numpy as np

from stingray import Crossspectrum, Lightcurve
from utils import CSVWriter, benchCode

warnings.filterwarnings("ignore")


def createCspec(lc1, lc2):
    Crossspectrum(lc1, lc2, dt=1.0)


def rebinCspec(cspec):
    cspec.rebin(df=2.0)


def coherCspec(cspec):
    cspec.coherence()


def TlagCspec(cspec):
    cspec.time_lag()


def CspecMain(bench_msg):
    func_dict = {
        'Crossspectrum': [
            'Time_Init', 'Mem_Init', 'Time_Rebin_Linear', 'Mem_Rebin_Linear',
            'Time_Coherence', 'Mem_Coherence', 'Time_Tlag', 'Mem_Tlag'
        ]
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

        time1, mem1 = benchCode(createCspec, lc, lc_other)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        cspec = Crossspectrum(lc, lc_other, dt=1.0)

        time1, mem1 = benchCode(rebinCspec, cspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(coherCspec, cspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(TlagCspec, cspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        del times, counts, lc, lc_other, cspec, time1, mem1

    CSVWriter(func_dict, wall_time, mem_use)
    del func_dict, wall_time, mem_use

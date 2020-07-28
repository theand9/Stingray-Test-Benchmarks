import time
import warnings
from datetime import datetime

import numpy as np

from stingray import Lightcurve, Powerspectrum
from utils import CSVWriter, benchCode

warnings.filterwarnings("ignore")


def createPspec(lc):
    Powerspectrum(lc)


def rebinPspec(pspec):
    pspec.rebin(df=0.01)


def classSign(pspec):
    pspec.classical_significances()


def pspecRMS(pspec):
    pspec.compute_rms(min_freq=min(pspec.freq) * 10,
                      max_freq=max(pspec.freq) / 1.5)


def PspecMain(bench_msg):
    func_dict = {
        'Powerspectrum': [
            'Time_Init', 'Mem_Init', 'Time_Rebin', 'Mem_Rebin', 'Time_RMS', 'Mem_RMS', 'Time_Class_Sign', 'Mem_Class_Sign'
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

        time1, mem1 = benchCode(createPspec, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        pspec = Powerspectrum(lc)

        time1, mem1 = benchCode(rebinPspec, pspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(pspecRMS, pspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        temp_pspec = Powerspectrum(lc, norm='leahy')
        time1, mem1 = benchCode(classSign, temp_pspec)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        del pspec, temp_pspec, lc, times, counts, time1, mem1

    CSVWriter(func_dict, wall_time, mem_use)
    del func_dict, wall_time, mem_use

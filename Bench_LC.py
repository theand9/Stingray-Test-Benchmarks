import time
import warnings
from datetime import datetime

import numpy as np

from stingray import Lightcurve
from utils import CSVWriter, benchCode

warnings.filterwarnings("ignore")


def makeLCFunc(times):
    Lightcurve.make_lightcurve(times, dt=1.0)


def createLc(times, counts):
    Lightcurve(times, counts)


def createLcP(times, counts):
    Lightcurve(times, counts, dt=1.0, skip_checks=True)


def lcMJD(lc_obj):
    lc_obj.change_mjdref(-2379826)


def rebinSum(lc_obj, dt_new):
    lc_obj.rebin(dt_new)


def rebinMean(lc_obj, dt_new):
    lc_obj.rebin(dt_new, method='mean')


def addLC(lc1, lc2):
    lc1.__add__(lc2)


def subLC(lc1, lc2):
    lc1.__sub__(lc2)


def eqLC(lc1, lc2):
    lc1.__eq__(lc2)


def negLC(lc1):
    lc1.__neg__()


def indexTrunc(lc):
    lc.truncate(0, lc.__len__() // 2)


def tTrunc(lc):
    lc.truncate(0, lc.__len__() // 2, method='time')


def splitLc(lc, min_gap):
    lc.split(min_gap)


def sortLcTime(lc):
    lc.sort()


def sortLcCount(lc):
    lc.sort_counts()


def chunkAnlyze(lc, chunk_len, target_func):
    lc.analyze_lc_chunks(chunk_len, target_func)


def chunkLen(lc, min_count, min_t_bins):
    lc.estimate_chunk_length(min_count, min_t_bins)


def joinLc(lc1, lc2):
    lc1.join(lc2)


def LCMain(bench_msg):
    func_dict = {
        'Lightcurve': [
            'Time_MakeLightcurve', 'Mem_MakeLightcurve', 'Time_InitNoParam',
            'Mem_InitNoParam', 'Time_InitParam', 'Mem_InitParam',
            'Time_ChangeMJDREF', 'Mem_ChangeMJDREF', 'Time_Rebin_Sum',
            'Mem_Rebin_Sum', 'Time_Rebin_Mean_Avg', 'Mem_Rebin_Mean_Avg',
            'Time_AddLC', 'Mem_AddLC', 'Time_SubLC', 'MemSubLC', 'Time_EqLC',
            'Mem_EqLC', 'Time_NegLC', 'Mem_NegLC', 'Time_Trunc_Index',
            'Mem_Trunc_Index', 'Time_Trunc_Time', 'Mem_Trunc_Time',
            'Time_SplitLC', 'Mem_SplitLC', 'Time_Sort_Time', 'Mem_Sort_Time',
            'Time_Sort_Counts', 'Mem_Sort_Counts', 'Time_Analyze_Chunks',
            'Mem_Analyze_Chunks', 'Time_Est_Chunk_Len', 'Mem_Est_Chunk_Len',
            'Time_JoinLC', 'Mem_JoinLC'
        ]}

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

        time1, mem1 = benchCode(makeLCFunc, times)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(createLc, times, counts)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(createLcP, times, counts)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        lc = Lightcurve(times, counts, dt=1.0, skip_checks=True)

        time1, mem1 = benchCode(lcMJD, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(rebinSum, lc, 2.0)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(rebinMean, lc, 2.0)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        lc_other = Lightcurve(times,
                              counts * np.random.rand(size),
                              dt=1.0,
                              skip_checks=True)

        time1, mem1 = benchCode(addLC, lc, lc_other)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(subLC, lc, lc_other)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(eqLC, lc, lc_other)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1
        del lc_other

        time1, mem1 = benchCode(negLC, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(indexTrunc, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(tTrunc, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        times2 = np.arange(0, size, np.random.randint(4, 9))
        counts2 = np.random.rand(len(times)) * 100
        lc_temp = Lightcurve(times, counts, dt=1.0, skip_checks=True)
        time1, mem1 = benchCode(splitLc, lc_temp, 4)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1
        del times2, counts2, lc_temp

        time1, mem1 = benchCode(sortLcTime, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(sortLcCount, lc)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(chunkAnlyze, lc, 100000, lambda x: np.mean(x))
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        time1, mem1 = benchCode(chunkLen, lc, 10000, 10000)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        lc_other = Lightcurve(times,
                              counts * np.random.rand(size),
                              dt=1.0,
                              skip_checks=True)

        time1, mem1 = benchCode(joinLc, lc, lc_other)
        wall_time[num_func].append(time1)
        mem_use[num_func].append(mem1)
        num_func += 1

        del lc, lc_other, time1, mem1, times, counts

    CSVWriter(func_dict, wall_time, mem_use)
    del func_dict, wall_time, mem_use

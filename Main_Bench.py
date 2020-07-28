import os

from Bench_AvgCspec import AvgCspecMain
from Bench_AvgPspec import AvgPspecMain
from Bench_Cspec import CspecMain
from Bench_LC import LCMain
from Bench_Pspec import PspecMain
from utils import CSVPlotter

if __name__ == "__main__":
    choice = int(input("\n1. Benchmark stingray \n2. Plot function times \nEnter your choice: "))

    if choice == 1:
        bench_msg = input("\nEnter the changes made, if none please enter None: ")

        LCMain(bench_msg)

        CspecMain(bench_msg)
        PspecMain(bench_msg)

        AvgCspecMain(bench_msg)
        AvgPspecMain(bench_msg)

    elif choice == 2:
        class_name = input("\nEnter the class whose function you wish to benchmark: ")
        file_name = input("Enter the function you wish to benchmark: ")
        CSVPlotter(os.path.abspath(os.getcwd()), class_name, file_name)

# run_trials.py

import random
import time
import csv
import os
import statistics

from sorting_algorithms import selection_sort, insertion_sort
from analysis_utils import run_t_test
from plotting_utils import generate_all_plots
from input_generator import (
    generate_random_array,
    generate_fixed_seed_array,
    generate_partially_sorted_array
)

def run_trials(sort_fn, input_size, num_trials=100, input_type="random", sorted_percent=50, unique=True, as_float=False):
    wall_times = []
    cpu_times = []
    comparisons = []
    swaps = []

    for trial in range(num_trials):
        # === Select input generation strategy ===
        if input_type == "random":
            arr = generate_random_array(input_size, unique=unique, as_float=as_float)
        elif input_type == "fixed":
            arr = generate_fixed_seed_array(input_size, seed=trial, as_float=as_float)
        elif input_type == "partial":
            arr = generate_partially_sorted_array(input_size, sorted_percent=sorted_percent, as_float=as_float)
        else:
            raise ValueError(f"Unknown input type: {input_type}")

        cpu_start = time.process_time()
        wall_start = time.perf_counter()

        _, comp_count, swap_count = sort_fn(arr.copy())

        wall_end = time.perf_counter()
        cpu_end = time.process_time()

        wall_times.append((wall_end - wall_start) * 1000)
        cpu_times.append((cpu_end - cpu_start) * 1000)
        comparisons.append(comp_count)
        swaps.append(swap_count)

    return wall_times, cpu_times, comparisons, swaps


def save_metrics_to_csv(filename, metrics, headers):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(zip(*metrics))

def print_statistics(name, times):
    print(f"\n{name} Runtime Stats (ms):")
    print(f"  Range: {max(times) - min(times):.2f}")
    print(f"  Mean: {statistics.mean(times):.2f}")
    print(f"  Median: {statistics.median(times):.2f}")
    print(f"  Std Dev: {statistics.stdev(times):.2f}")

def main():
    input_size = 5000
    num_trials = 100

    # ==== Input config ====
    input_type = "partial"       # Options: "random", "fixed", "partial"
    sorted_percent = 75          # Only for "partial"
    unique = False               # False = includes duplicates
    as_float = False             # True = float input instead of int

    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    print("Running Selection Sort...")
    sel_wall, sel_cpu, sel_cmp, sel_swp = run_trials(
        selection_sort, input_size, num_trials,
        input_type=input_type,
        sorted_percent=sorted_percent,
        unique=unique,
        as_float=as_float
    )
    save_metrics_to_csv("data/selection_sort.csv",
        [sel_wall, sel_cpu, sel_cmp, sel_swp],
        ["Wall Time (ms)", "CPU Time (ms)", "Comparisons", "Swaps"])
    print_statistics("Selection Sort", sel_wall)

    print("Running Insertion Sort...")
    ins_wall, ins_cpu, ins_cmp, ins_swp = run_trials(
        insertion_sort, input_size, num_trials,
        input_type=input_type,
        sorted_percent=sorted_percent,
        unique=unique,
        as_float=as_float
    )
    save_metrics_to_csv("data/insertion_sort.csv",
        [ins_wall, ins_cpu, ins_cmp, ins_swp],
        ["Wall Time (ms)", "CPU Time (ms)", "Comparisons", "Swaps"])
    print_statistics("Insertion Sort", ins_wall)

    run_t_test(sel_wall, ins_wall, "Selection Sort", "Insertion Sort")

    metric_names = ["Wall Time (ms)", "CPU Time (ms)", "Comparisons", "Swaps"]
    generate_all_plots(
        selection_data=[sel_wall, sel_cpu, sel_cmp, sel_swp],
        insertion_data=[ins_wall, ins_cpu, ins_cmp, ins_swp],
        metric_names=metric_names,
        output_dir="plots"
    )

if __name__ == "__main__":
    main()

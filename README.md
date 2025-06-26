PERFORMANCE ANALYSIS OF SELECTION SORT vs INSERTION SORT

OBJECTIVE
This research evaluates and compares the performance characteristics of two quadratic complexity sorting algorithms: Selection Sort and Insertion Sort. Key performance metrics including CPU time, wall clock time, comparisons, swaps, and relative performance to Python's built-in sort were analyzed. A randomized dataset of 1,000 integers was used, and each algorithm was executed 100 times to ensure consistent and accurate timing results. All data, metrics, graphs, and formulas were derived from a Python program built for this study.

INTRODUCTION
Sorting algorithms are essential in computer science for organizing data. While efficient algorithms like Merge Sort and exist, analyzing basic algorithms like Selection Sort and Insertion Sort provides foundational insights. This study focuses on their performance on a large, randomized dataset.

METHODOLOGY
Test Setup
•	Language: Python 3.x
•	Dataset: 1,000 random integers stored in data/input_data.txt
•	Repeats per test: 100 times per algorithm
•	Metrics captured: CPU time, wall time, swaps, comparisons, ratio to built-in sort
•	Graphs exported: wall time, CPU time, comparisons, swaps, ratio vs built-in
•	Output CSV: data/sort_results.csv
Tools Used
•	Python built-in libraries: time, csv, os, matplotlib.pyplot
•	Graphs saved using matplotlib
•	Timing with time.process_time() and time.time()
•	Comparison and swap counts instrumented inside sorting functions
Input Data 
Random integers between 1–999, saved in input_data.txt. Sample:
663 551 985 442 24 776 990 450 288 897 535 58 159 626 49 792 464 301 279 616 ... (1000 total)






FORMULA
Metric Computation
To obtain statistically significant timing data, we computed the arithmetic mean over 100 repetitions.
Mean CPU Time




Where:
•	Ti= CPU time for the ith run
•	N=100
Relative Ratio vs Built-in Sort

Ratio = Talgorithm / Tbuiltin
Where:
•	Talgorithm= Mean CPU time for Selection/Insertion Sort.
•	Tbuiltin= Mean CPU time for Python’s built-in sort.

Selection Sort Comparisons
Cselection= n(n-1)/2
For n=1000, C=499,500.
Insertion Sort comparisons vary depending on initial order:
•	Best case: n−1
•	Worst case: n(n−1)/2
•	Our randomized data falls in between

Average Swaps/Comparisons
Average=Total over all runs/n 

CODE LISTING
Source Code: The Python script sort_experiment.py contains all logic for:
•	Selection Sort and Insertion Sort implementation
•	Measuring CPU time, wall time, swaps, and comparisons
•	Generating plots using matplotlib
•	Exporting results to CSV and graph files
Support files:
•	data/input_data.txt — contains 1,000 random integers
•	data/sort_results.csv — stores all measured output
•	plots/ stores bar charts comparing sorting performance


import time
import os
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

# ---------- Ensure folders exist ----------
os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# ---------- Read input data from text file ----------
def read_array_from_file(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
        elements = content.replace('\n', ' ').split()
        return [int(e) for e in elements if e.strip().isdigit()]

# ---------- Metrics ----------
class SortMetrics:
    def __init__(self):
        self.swaps = 0
        self.comparisons = 0

# ---------- Sorting algorithms ----------
def selection_sort(arr, metrics):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            metrics.comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if i != min_idx:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            metrics.swaps += 1

def insertion_sort(arr, metrics):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            metrics.comparisons += 1
            arr[j + 1] = arr[j]
            metrics.swaps += 1
            j -= 1
        metrics.comparisons += 1
        arr[j + 1] = key

# ---------- Timed runs with averaging ----------
def run_test(sort_fn, arr, repeats=100):
    metrics = SortMetrics()
    total_cpu = 0
    total_wall = 0

    for _ in range(repeats):
        arr_copy = arr.copy()
        start_wall = time.time()
        start_cpu = time.process_time()
        sort_fn(arr_copy, metrics)
        end_wall = time.time()
        end_cpu = time.process_time()
        total_wall += (end_wall - start_wall)
        total_cpu += (end_cpu - start_cpu)

    return {
        'wall_time': total_wall / repeats,
        'cpu_time': total_cpu / repeats,
        'swaps': metrics.swaps // repeats,
        'comparisons': metrics.comparisons // repeats
    }

def time_builtin_sort(arr, repeats=100):
    total_cpu = 0
    for _ in range(repeats):
        arr_copy = arr.copy()
        start = time.process_time()
        arr_copy.sort()
        end = time.process_time()
        total_cpu += (end - start)
    return total_cpu / repeats

# ---------- Experiment ----------
def experiment():
    arr = read_array_from_file("data/input_data.txt")
    results = []

    builtin_time = time_builtin_sort(arr, repeats=100)
    print(f"Average Built-in sort CPU time: {builtin_time:.10f}")

    sel_result = run_test(selection_sort, arr, repeats=100)
    ins_result = run_test(insertion_sort, arr, repeats=100)

    sel_result['algo'] = 'Selection'
    ins_result['algo'] = 'Insertion'

    # Prevent divide by zero
    safe_builtin_time = builtin_time if builtin_time > 0 else 1e-9
    sel_result['ratio_vs_builtin'] = sel_result['cpu_time'] / safe_builtin_time
    ins_result['ratio_vs_builtin'] = ins_result['cpu_time'] / safe_builtin_time

    results.append(sel_result)
    results.append(ins_result)
    return results

# ---------- Summary ----------
def summarize_results(results):
    grouped = defaultdict(list)
    for result in results:
        grouped[result['algo']].append(result)

    for algo, runs in grouped.items():
        wall_times = [r['wall_time'] for r in runs]
        cpu_times = [r['cpu_time'] for r in runs]
        swaps = [r['swaps'] for r in runs]
        comps = [r['comparisons'] for r in runs]
        ratios = [r['ratio_vs_builtin'] for r in runs]

        print(f"\n--- {algo} Sort Summary ---")
        print(f"Wall Time: {wall_times[0]:.6f}s")
        print(f"CPU Time: {cpu_times[0]:.6f}s")
        print(f"Swaps: {swaps[0]}")
        print(f"Comparisons: {comps[0]}")
        print(f"Ratio vs Built-in: {ratios[0]:.2f}")
        print()

# ---------- CSV Export ----------
def export_to_csv(results, filename="data/sort_results.csv"):
    keys = ['algo', 'wall_time', 'cpu_time', 'swaps', 'comparisons', 'ratio_vs_builtin']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Results exported to {filename}")

# ---------- Plotting ----------
def plot_results(results):
    selection = [r for r in results if r['algo'] == 'Selection']
    insertion = [r for r in results if r['algo'] == 'Insertion']

    def extract(metric):
        return [r[metric] for r in selection], [r[metric] for r in insertion]

    wall_sel, wall_ins = extract('wall_time')
    cpu_sel, cpu_ins = extract('cpu_time')
    ratio_sel, ratio_ins = extract('ratio_vs_builtin')
    comps_sel, comps_ins = extract('comparisons')
    swaps_sel, swaps_ins = extract('swaps')

    def save_bar_plot(values, title, ylabel, filename):
        plt.figure()
        plt.bar(['Selection', 'Insertion'], values, color=['blue', 'orange'])
        for i, v in enumerate(values):
            plt.text(i, v + 0.01 * max(values), f"{v:.5f}" if isinstance(v, float) else str(v),
                     ha='center', va='bottom', fontsize=10)
        plt.title(title)
        plt.ylabel(ylabel)
        plt.savefig(f"plots/{filename}")
        plt.close()

    save_bar_plot(wall_sel + wall_ins, 'Wall Time Comparison', 'Seconds', 'wall_time_comparison.png')
    save_bar_plot(cpu_sel + cpu_ins, 'CPU Time Comparison', 'Seconds', 'cpu_time_comparison.png')
    save_bar_plot(ratio_sel + ratio_ins, 'Relative CPU Time vs Built-in Sort', 'Ratio', 'ratio_vs_builtin.png')
    save_bar_plot(comps_sel + comps_ins, 'Number of Comparisons', 'Comparisons', 'comparisons_count.png')
    save_bar_plot(swaps_sel + swaps_ins, 'Number of Swaps', 'Swaps', 'swaps_count.png')

    print("All plots saved in /plots/ folder.")

# ---------- Main ----------
if __name__ == "__main__":
    results = experiment()
    summarize_results(results)
    export_to_csv(results)
    plot_results(results)


RESULTS
Algorithm	CPU Time (s)	Wall Time (s)	Comparisons	Swaps	Ratio vs Built-in
Selection Sort	0.00372	0.00482	499,500	999	9.30
Insertion Sort	0.00458	0.00514	253,111	1253	11.45

•	wall_time_comparison.png
•	cpu_time_comparison.png
•	ratio_vs_builtin.png
•	comparisons_count.png
•	swaps_count.png
 
 


   



DISCUSSION
Selection Sort has predictable comparison counts but fewer swaps. Insertion Sort is adaptive to data order and can perform better when data is partially sorted. However, both algorithms are significantly slower than modern hybrid sorts like Timsort. Graphs clearly show the tradeoff between swaps and comparisons.

CONCLUSION 
While quadratic algorithms are educational, they are impractical for large datasets. This study reinforces the importance of algorithm selection based on data size and structure. Repeated trials with statistical averaging are essential for accurate performance measurement.





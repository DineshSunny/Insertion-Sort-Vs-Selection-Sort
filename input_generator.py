# input_generator.py

import random

def generate_random_array(size, unique=True, as_float=False):
    if unique:
        arr = random.sample(range(1, size * 10), size)
    else:
        base = [random.randint(1, size // 2) for _ in range(size)]
        arr = base

    if as_float:
        arr = [float(x) for x in arr]
    return arr

def generate_partially_sorted_array(size, sorted_percent=50, as_float=False):
    arr = list(range(size))
    num_sorted = int((sorted_percent / 100.0) * size)
    num_unsorted = size - num_sorted

    sorted_part = arr[:num_sorted]
    unsorted_part = arr[num_sorted:]
    random.shuffle(unsorted_part)

    combined = sorted_part + unsorted_part
    if as_float:
        combined = [float(x) for x in combined]
    return combined

def generate_fixed_seed_array(size, seed=42, as_float=False):
    random.seed(seed)
    arr = random.sample(range(1, size * 10), size)
    if as_float:
        arr = [float(x) for x in arr]
    return arr

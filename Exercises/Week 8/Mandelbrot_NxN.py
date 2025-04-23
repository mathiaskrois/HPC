#!/usr/bin/env python3

import sys
import numpy as np
import multiprocessing

def mandelbrot_value(c, max_iter=256):
    """Returns the iteration count at which |z|>2, or max_iter if never."""
    z = 0 + 0j
    for i in range(max_iter):
        if (z.real*z.real + z.imag*z.imag) > 4.0:
            return i
        z = z*z + c
    return max_iter

def compute_rows(args):
    """
    Each process handles rows [row_start, row_end) of the NxN memmap.
    """
    (filename, N, row_start, row_end,
     real_min, real_max, imag_min, imag_max, max_iter) = args

    # Open the existing memmap in r+ (read/write) mode:
    mandel_memmap = np.memmap(filename, dtype=np.uint16, mode='r+', shape=(N, N))

    real_range = real_max - real_min
    imag_range = imag_min - imag_max  # or imag_max - imag_min, see below

    # Careful with the sign; typical domain is imag_min<imag_max
    # so the range is (imag_max - imag_min).
    # We'll do:
    imag_range = (imag_max - imag_min)

    for row in range(row_start, row_end):
        y = imag_min + (row / (N - 1)) * imag_range
        for col in range(N):
            x = real_min + (col / (N - 1)) * real_range
            c = complex(x, y)
            mandel_memmap[row, col] = mandelbrot_value(c, max_iter)

    mandel_memmap.flush()
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python mandelbrot_memmap.py <N> [<num_processes>]")
        sys.exit(1)

    N = int(sys.argv[1])
    num_processes = 1
    if len(sys.argv) == 3:
        num_processes = int(sys.argv[2])

    filename = "mandelbrot.raw"
    # Create the file/truncate it with the right shape:
    mandel_memmap = np.memmap(filename, dtype=np.uint16, mode='w+', shape=(N, N))
    mandel_memmap.flush()

    # Domain settings:
    real_min, real_max = -2.0, 1.0
    imag_min, imag_max = -1.0, 1.0
    max_iter = 256

    # Divide the rows among processes:
    chunk_size = N // num_processes
    tasks = []
    start_row = 0
    for i in range(num_processes):
        end_row = start_row + chunk_size
        if i == num_processes - 1:  # last chunk
            end_row = N
        tasks.append((filename, N, start_row, end_row,
                      real_min, real_max, imag_min, imag_max, max_iter))
        start_row = end_row

    with multiprocessing.Pool(num_processes) as pool:
        pool.map(compute_rows, tasks)

if __name__ == "__main__":
    main()

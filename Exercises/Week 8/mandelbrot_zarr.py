#!/usr/bin/env python3

import sys
import math
import numpy as np
import zarr
import multiprocessing

def mandelbrot_value(c, max_iter=256):
    """Compute the number of iterations at which |z|>2, or max_iter if never."""
    z = 0 + 0j
    for i in range(max_iter):
        if (z.real*z.real + z.imag*z.imag) > 4.0:
            return i
        z = z*z + c
    return max_iter

def fill_chunk(args):
    """
    Each process fills a single (chunk_row, chunk_col) chunk in the Zarr array.
    """
    (store_path, N, C, chunk_row, chunk_col,
     real_min, real_max, imag_min, imag_max, max_iter) = args

    # Open the zarr in r+ mode (it already exists, we just fill data):
    z = zarr.open(store_path, mode='r+')

    row_start = chunk_row * C
    row_end   = min(row_start + C, N)
    col_start = chunk_col * C
    col_end   = min(col_start + C, N)

    real_range = real_max - real_min
    imag_range = imag_max - imag_min

    for row in range(row_start, row_end):
        y = imag_min + (row / (N - 1)) * imag_range
        for col in range(col_start, col_end):
            x = real_min + (col / (N - 1)) * real_range
            val = mandelbrot_value(complex(x, y), max_iter)
            z[row, col] = val

def main():
    if len(sys.argv) < 3:
        print("Usage: python mandelbrot_zarr.py <N> <C> [<num_processes>]")
        sys.exit(1)

    N = int(sys.argv[1])
    C = int(sys.argv[2])
    num_processes = 1
    if len(sys.argv) == 4:
        num_processes = int(sys.argv[3])

    store_path = "mandelbrot.zarr"

    # Create the zarr array with shape (N,N) and chunk shape (C,C).
    z = zarr.open(store_path, mode='w', shape=(N, N), chunks=(C, C), dtype='uint16')

    real_min, real_max = -2.0, 1.0
    imag_min, imag_max = -1.0, 1.0
    max_iter = 256

    # Figure out how many chunk rows/cols we have:
    chunk_rows = math.ceil(N / C)
    chunk_cols = math.ceil(N / C)

    # Build a list of chunk tasks:
    tasks = []
    for cr in range(chunk_rows):
        for cc in range(chunk_cols):
            tasks.append(
                (store_path, N, C, cr, cc,
                 real_min, real_max, imag_min, imag_max, max_iter)
            )

    # Distribute the chunk computations in parallel:
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(fill_chunk, tasks)

if __name__ == "__main__":
    main()

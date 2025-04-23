#!/usr/bin/env python3

import sys
import numpy as np
from PIL import Image

def main():
    if len(sys.argv) != 4:
        print("Usage: python handin.py <raw_file> <N> <step>")
        sys.exit(1)

    raw_file = sys.argv[1]
    N = int(sys.argv[2])
    step = int(sys.argv[3])

    data = np.fromfile(raw_file, dtype=np.uint32)
    if data.size != N * N:
        raise ValueError(f"Expected {N*N} elements, but got {data.size}.")

    arr = data.reshape((N, N))

    downsampled = arr[::step, ::step]

    max_val = downsampled.max() if downsampled.size else 1
    if max_val == 0:
        max_val = 1
    scaled = (downsampled * 255 // max_val).astype(np.uint8)

    img = Image.fromarray(scaled, mode='L')
    img.save("out.png")

if __name__ == "__main__":
    main()

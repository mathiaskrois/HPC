#!/usr/bin/env python3

import sys
import pandas as pd


def main():
    if len(sys.argv) != 3:
        print("Usage: python chunk_data.py <csv_file> <chunk_size>")
        sys.exit(1)

    csv_file = sys.argv[1]
    chunk_size = int(sys.argv[2])

    total_precip = 0.0

    # Read the CSV in chunks without loading it all into memory:
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size):

        total_precip += chunk["value"].sum()

    print(total_precip)


if __name__ == "__main__":
    main()

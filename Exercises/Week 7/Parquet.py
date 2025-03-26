import sys
import os
import pandas as pd

def csv_to_parquet(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    parquet_path = csv_path.replace('.csv', '.parquet')
    df.to_parquet(parquet_path)

    csv_size = os.path.getsize(csv_path)
    parquet_size = os.path.getsize(parquet_path)

    size_difference = csv_size - parquet_size

    print(f"CSV file size: {csv_size / (1024 ** 2):.2f} MB")
    print(f"Parquet file size: {parquet_size / (1024 ** 2):.2f} MB")
    print(f"Size difference: {size_difference / (1024 ** 2):.2f} MB")

if __name__ == '__main__':
    csv_to_parquet(sys.argv[1])
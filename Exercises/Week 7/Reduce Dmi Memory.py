import sys
import pandas as pd

def total_precipitation(csv_path: str) -> None:
    df = pd.read_csv(csv_path)
    total_precip = df.loc[df['parameterId'] == 'precip_past10min', 'value'].sum()
    print(total_precip)

if __name__ == '__main__':
    total_precipitation(sys.argv[1])

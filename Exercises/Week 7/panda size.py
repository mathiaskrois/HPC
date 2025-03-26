def df_memsize(df):
    size = df.memory_usage(index=True, deep=True).sum()

    return size


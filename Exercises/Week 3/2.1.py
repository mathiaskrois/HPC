import sys
import time
import os
import blosc
import numpy as np

def write_numpy(arr, fname):
    np.save(fname + ".npy", arr)
    os.sync()

def write_blosc(arr, fname, cname="lz4"):
    b = blosc.pack_array(arr, cname=cname)
    with open(fname + ".bl", "wb") as w:
        w.write(b)
    os.sync()

def read_numpy(fname):
    return np.load(fname + ".npy")

def read_blosc(fname):
    with open(fname + ".bl", "rb") as r:
        b = r.read()
    return blosc.unpack_array(b)

n = int(sys.argv[1])
arr = np.zeros((n,n,n), dtype='uint8')

t0 = time.perf_counter()
write_numpy(arr, "test")
t1 = time.perf_counter()
wn = t1 - t0

t0 = time.perf_counter()
write_blosc(arr, "test")
t1 = time.perf_counter()
wb = t1 - t0

t0 = time.perf_counter()
a1 = read_numpy("test")
t1 = time.perf_counter()
rn = t1 - t0

t0 = time.perf_counter()
a2 = read_blosc("test")
t1 = time.perf_counter()
rb = t1 - t0

print(wn, wb, rn, rb)

import ctypes
import multiprocessing as mp
import sys
from time import perf_counter as time
import numpy as np
from PIL import Image


def init(shared_arr_):
    global shared_arr
    shared_arr = shared_arr_


def tonumpyarray(mp_arr):
    return np.frombuffer(mp_arr, dtype='float32')


def reduce_step(args):
    i, stride, elemshape = args
    arr = tonumpyarray(shared_arr).reshape((-1,) + elemshape)
    # Add arr[i + stride] to arr[i], checking bounds
    if i + stride < arr.shape[0]:
        arr[i] += arr[i + stride]


if __name__ == '__main__':
    n_processes = 4  # Example number of processes
    data = np.load(sys.argv[1])
    elemshape = data.shape[1:]
    shared_arr = mp.RawArray(ctypes.c_float, data.size)

    # Copy numpy data into shared memory
    arr = tonumpyarray(shared_arr).reshape(data.shape)
    np.copyto(arr, data)
    del data

    # Start parallel pool
    pool = mp.Pool(n_processes, initializer=init, initargs=(shared_arr,))

    # Perform the full parallel reduction
    t_start = time()
    stride = 1
    N = arr.shape[0]
    while stride < N:
        # Build list of tasks, jumping in steps of 2*stride
        tasks = [(i, stride, elemshape) for i in range(0, N, 2 * stride)]
        pool.map(reduce_step, tasks, chunksize=1)
        stride *= 2

    # Now arr[0] holds the sum over all images. Divide by N to get mean
    arr[0] /= N

    print("Reduction + mean time:", time() - t_start)

    # Save the first image (the average face) as result.png
    final_image = arr[0]
    Image.fromarray((255 * final_image).astype('uint8')).save('result.png')

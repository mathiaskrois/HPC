@cuda.jit
def add_kernel(x, y, out):
    idx = cuda.grid(1)  # Compute the global thread index
    if idx < x.size:    # Ensure we don't go out of bounds
        out[idx] = x[idx] + y[idx]
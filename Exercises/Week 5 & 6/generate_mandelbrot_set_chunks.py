import multiprocessing
import numpy as np
import matplotlib.pyplot as plt

def mandelbrot_escape_time(c):
    z = 0
    for i in range(100):
        z = z**2 + c
        if np.abs(z) > 2.0:
            return i
    return 100

def compute_chunk(chunk):
    return [mandelbrot_escape_time(c) for c in chunk]

def generate_mandelbrot_set(points, num_processes):
    chunk_size = len(points) // num_processes  # Base chunk size
    chunks = [points[i * chunk_size : (i + 1) * chunk_size] for i in range(num_processes)]

    remainder = len(points) % num_processes
    if remainder > 0:
        chunks[-1] = np.concatenate([chunks[-1], points[-remainder:]])

    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(compute_chunk, chunks)

    return np.array([val for sublist in results for val in sublist])  # Flatten results

def generate_mandelbrot_set_chunks(points, num_processes, chunk_size=10000):
    chunks = [points[i : i + chunk_size] for i in range(0, len(points), chunk_size)]

    with multiprocessing.Pool(num_processes) as pool:
        results = pool.map(compute_chunk, chunks)

    return np.array([val for sublist in results for val in sublist])  # Flatten results

def plot_mandelbrot(escape_times):
    plt.imshow(escape_times, cmap='hot', extent=(-2, 2, -2, 2))
    plt.axis('off')
    plt.savefig('mandelbrot.png', bbox_inches='tight', pad_inches=0)

if __name__ == "__main__":
    width = 800
    height = 800
    xmin, xmax = -2, 2
    ymin, ymax = -2, 2
    num_proc = 4
    chunk_size = 10000

    # Precompute points
    x_values = np.linspace(xmin, xmax, width)
    y_values = np.linspace(ymin, ymax, height)
    points = np.array([complex(x, y) for x in x_values for y in y_values])

    # Compute Mandelbrot set using smaller chunks
    mandelbrot_set = generate_mandelbrot_set_chunks(points, num_proc, chunk_size)

    # Save Mandelbrot set as an image
    mandelbrot_set = mandelbrot_set.reshape((height, width))
    plot_mandelbrot(mandelbrot_set)

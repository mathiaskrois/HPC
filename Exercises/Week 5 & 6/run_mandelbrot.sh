#!/bin/bash
#BSUB -J mandelbrot_test
#BSUB -q hpc
#BSUB -W 0:10
#BSUB -n 16  # Request up to 16 cores
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model==XeonGold6142]"
#BSUB -o mandelbrot_%J.out
#BSUB -e mandelbrot_%J.err

module purge
module load python/3.9.0

# Create output file
echo "num_proc,real_time" > mandelbrot_results.csv

# Run the program with varying num_proc values
for num_proc in 1 2 4 8 16
do
    echo "Running Mandelbrot with num_proc=$num_proc"
    export NUM_PROC=$num_proc
    { time python mandelbrot_parallel.py $NUM_PROC ; } 2>&1 | awk '/real/ {print "'$num_proc'," $2}' >> mandelbrot_results.csv
done

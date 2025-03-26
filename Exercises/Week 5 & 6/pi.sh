#!/bin/bash
#BSUB -J pi_test
#BSUB -q hpc
#BSUB -W 0:10
#BSUB -n 10
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model==XeonGold6142]"
#BSUB -o pi_test_%J.out
#BSUB -e pi_test_%J.err

module purge
module load python/3.9.0

echo "Running Serial Implementation"
time python serial_pi.py

echo "Running Fully Parallel Implementation"
time python parallel_pi.py

echo "Running Chunked Parallel Implementation"
time python chunked_parallel_pi.py

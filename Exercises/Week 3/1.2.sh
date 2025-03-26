#!/bin/bash
#BSUB -J cache_test
#BSUB -q hpc
#BSUB -W 0:10
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "select[model==XeonGold6142]"
#BSUB -o cache_test_%J.out
#BSUB -e cache_test_%J.err
module purge
module load python/3.9.0
python cache_performance.py

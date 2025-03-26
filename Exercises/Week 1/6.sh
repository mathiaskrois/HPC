#!/bin/bash
#BSUB -J cpu_64core_test
#BSUB -q hpc
#BSUB -W 2
#BSUB -n 64
#BSUB -R "span[hosts=1]" 
#BSUB -o cpu_64core_test_%J.out
#BSUB -e cpu_64core_test_%J.err

echo "Job running on node: $(hostname)"
echo "Number of CPU cores allocated:"
grep -c ^processor /proc/cpuinfo

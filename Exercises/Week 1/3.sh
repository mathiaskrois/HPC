#!/bin/bash
#BSUB -J cpu_test
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "select[model==XeonGold6126]"
#BSUB -o cpu_test_%J.out
#BSUB -e cpu_test_%J.err

echo "Job running on node: $(hostname)"
echo "CPU type:"
lscpu | grep "Model name"

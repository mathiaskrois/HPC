#!/bin/bash
#BSUB -J sleeper
#BSUB -q hpc
#BSUB -W 2
#BSUB -R "rusage[mem=512MB]"
#BSUB -o sleeper_%J.out
#BSUB -e sleeper_%J.err

# Email notification settings
#BSUB -u s214422@student.dtu.com
#BSUB -B
#BSUB -N

echo "Job started at $(date)"
sleep 60
echo "Job finished at $(date)"

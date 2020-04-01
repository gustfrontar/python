#!/bin/bash            
#SBATCH -p pps         
#SBATCH -J OpenMP      
#SBATCH -t 24:00:00    
#SBATCH -c 20          
#SBATCH --mem 30000    
export OMP_NUM_THREADS=30 
python compute_update_comparison.py  
from daostarfinder_dotdetection import dot_detection_parallel
from pathlib import Path
import os
from webfish_tools.util import find_matching_files
import numpy as np

JOB_ID = os.getenv('SLURM_ARRAY_TASK_ID', 0)

print(f'This is task {JOB_ID}')

directory = Path('$USERINPUT$/notebook_pyfiles/pre_processed_images/')
position_name = f'MMStack_Pos{JOB_ID}.ome.tif'

files, _, _ = find_matching_files(directory, 'HybCycle_{hyb}' + f'/{position_name}')
files = [str(f) for f in files]

HybCycle = JOB_ID
size_cutoff = 3 # sigma cutoff for size distribution
channels = np.arange(1,$CHANNELNUM$)#[1,2,3] #which channel to analyze
pos_start = $POS_START$ #referring to pos from find thresh
pos_end = $POS_STOP$ #referring to pos from find thresh (exclusive)
choose_thresh_sets = [$THRESHLIST$]#[10,10,10] #select best thresh set
hyb_number= $NUM_HYB$ #total number of hybs
check_initial = False #ignore unless you are trying to visualize
optimize=False #are you testing thresholds
output=True #do you want to write out results


for channel,choose_thresh_set in zip(channels, choose_thresh_sets):
    dot_detection_parallel(files, HybCycle,size_cutoff,channel,pos_start,pos_end,
                           choose_thresh_set,hyb_number, check_initial, optimize, output)

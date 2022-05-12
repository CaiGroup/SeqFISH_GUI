from daostarfinder_dotdetection import dot_detection_parallel
from pathlib import Path
import os
from webfish_tools.util import find_matching_files
import numpy as np 

JOB_ID = os.getenv('SLURM_ARRAY_TASK_ID', 0)

print(f'This is task {JOB_ID}')

#path for 1 pos
directory = Path('$USERINPUT$notebook_pyfiles/pre_processed_images/')
position_name = 'MMStack_Pos$CENTPOS$.ome.tif'
file = str(directory / f'HybCycle_{JOB_ID}'/ position_name) 

#arguments
HybCycle = JOB_ID
size_cutoff = 3 # sigma cutoff for size distribution
channels = np.arange(1,$CHANNELNUM$) #which channel to analyze (1-4)
pos_start = $POS_START$ #referring to pos from find thresh
pos_end = $POS_STOP$#referring to pos from find thresh (exclusive)
choose_thresh_set = 0 #ignore for optimization
hyb_number = $HYBTOT$ #total number of hybs
check_initial = False #ignore for optimization
optimize = True #are you testing thresholds
output = True #do you want to write out results

for channel in channels:
    dot_detection_parallel(file, HybCycle, size_cutoff,channel,pos_start,pos_end,choose_thresh_set,hyb_number,check_initial, optimize, output)
    save=1

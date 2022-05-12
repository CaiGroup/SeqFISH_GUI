from dash_radial_decoding import dash_radial_decoding
import os
import pandas as pd
import numpy as np
import glob

JOB_ID = os.getenv('SLURM_ARRAY_TASK_ID', 0)

print(f'This is task {JOB_ID}')

#fill parameters
locations_temp = f'$USERENT$notebook_pyfiles/dots_comb/final/Channel_CHANNEL_NUM/MMStack_Pos{JOB_ID}/*'
codebook_temp = f'$USERENT$notebook_pyfiles/codebooks_converted/channel_CHANNEL_NUM_converted.csv'
n_neighbors = 4
num_barcodes = 4
#multiply radius by 100 to get search in nm
first_radius=1
second_radius=2
diff=1
min_seed=3
hybs = $HYBTOT$
include_undecoded = False
triple_decode = True
output_temp = f'$USERENT$notebook_pyfiles/decoded/final_CHCHANNEL_NUM/MMStack_Pos{JOB_ID}'
channels = np.arange(1, $CHANNELNUM$)


for channel in channels:
    locations_path = glob.glob(locations_temp.replace('CHANNEL_NUM', str(channel)))
    codebook_path = codebook_temp.replace('CHANNEL_NUM', str(channel))
    output_dir =output_temp.replace('CHANNEL_NUM', str(channel))
    
    
    if len(locations_path) > 1:
        for locations in locations_path:
            dash_radial_decoding(locations, codebook_path, n_neighbors,
                                 num_barcodes, first_radius, second_radius,
                                 diff, min_seed, hybs,
                                 output_dir, include_undecoded, triple_decode)
    else:
        dash_radial_decoding(locations_path[0], codebook_path, n_neighbors,
                             num_barcodes, first_radius, second_radius,
                             diff, min_seed, hybs,
                             output_dir, include_undecoded, triple_decode)
        

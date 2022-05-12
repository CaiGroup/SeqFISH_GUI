from dapi_alignment_parallel import dapi_alignment_parallel
from pathlib import Path
import os
from webfish_tools.util import find_matching_files

JOB_ID = os.getenv('SLURM_ARRAY_TASK_ID', 0)

print(f'This is task {JOB_ID}')

#general path and position name
directory = Path('$FILENAME$')
position_name = f'MMStack_Pos{JOB_ID}.ome.tif'

##get all hybs with same position
##use this for background alignment
ref = directory / 'initial_background' /position_name

#use this for all hyb alignment
files, _, _ = find_matching_files(directory, 'HybCycle_{hyb}' + f'/{position_name}')
files = [str(f) for f in files]


image_ref = str(ref)
images_moving=files

dapi_alignment_parallel(image_ref,images_moving)

import os
import getpass 
import time
import numpy as np
from daostarfinder_dotdetection import combine_dot_files


def get_queue():
    jobs_running = [(i[:25]).replace(' ','') for i in os.popen('squeue -u '+getpass.getuser()).readlines()[1:]]
    if len(jobs_running) == 0:
        jobs_running.append('none')
    return jobs_running

def run_batch_files(batch_sets):
    for batch_set in batch_sets:
        directory = batch_set.split('/')[0]
        batch = batch_set.split('/')[1]

        cmd = ('cd #dir# && sbatch #batch#').replace('#dir#',directory).replace('#batch#',batch)
        batch_run = os.popen(cmd).readlines()[0]
        batch_run = batch_run.replace('Submitted batch job ', '').replace('\n','')
        while sum([batch_run in i for i in get_queue()]) > 0:
            time.sleep(60)
            print(batch+ ' sets still running.')
        print(batch+ ' has completed running.')

batch_sets = ['dot_detection_files/dotdetection_individual.batch']
run_batch_files(batch_sets)

##### Combine Dots
                  
import numpy as np
#c is referring to channels
for c in np.arange(1,#CHANNELNUM#):
    path_dots = f'#USERINPUT#notebook_pyfiles/dots_detected/final/Channel_{c}'
    #i is number of pos
    for i in np.arange(#POSNUM#):
        combine_dot_files(path_dots, hyb_start=#HYB_START#,hyb_end=#HYB_END#,num_HybCycle = #NUM_HYB#,
                  pos = i, channel=c, num_z = 1, opt_files = False)
        
        
run_batch_files(['decoding_files/dash_radial_decoding_AFTER_OPTIMIZATION.batch'])

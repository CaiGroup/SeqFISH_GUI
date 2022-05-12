import os
import getpass 
import time
import numpy as np
from barcode_key_converter import barcode_key_converter_within
import pandas as pd


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
        
user_path = '$DATA_DIR$'
make_codebooks = $MAKE_CODEBOOKS$

if 'notebook_pyfiles' not in os.listdir(user_path):
    os.system('cd ' + user_path + ' && mkdir notebook_pyfiles')
if 'codebooks_converted' not in os.listdir(user_path +'notebook_pyfiles' ):
    os.system('cd ' + user_path +'notebook_pyfiles'+ ' && mkdir codebooks_converted')

if make_codebooks:
    path_source = '$PATH_USER$'
    codebooks = 'channel_{CHANNEL_NUM}.csv'
    channels = np.arange(1, $CHANNELNUM$)

    for channel in channels:
        cdbk = codebooks.replace('{CHANNEL_NUM}', str(channel))
        old_codebook = pd.read_csv(path_source+cdbk).set_index('gene name')
        codebook = barcode_key_converter_within(old_codebook,num_hybs=$HYB_COUNT$,num_barcodes = $Barcode_COUNT$, ch=channel)
        codebook.to_csv(user_path +'notebook_pyfiles/codebooks_converted/'+cdbk.replace('.csv','') + '_converted'+'.csv')
    
    
batch_sets = ['dapi_alignment_files/dapi_align.batch', 'preprocessing_files/correct_many.batch']
run_batch_files(batch_sets)

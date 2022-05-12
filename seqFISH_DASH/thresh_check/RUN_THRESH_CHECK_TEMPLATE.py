import numpy as np
from datascience import *

channels = [$CHANNEL_NUM$]
index = []
FPR_lists = []
for channel in channels:
    data_dir = ('$USER_ENT$notebook_pyfiles/decoded/OPT_CH{CH}/MMStack_Pos{tnum}').replace('{CH}',str(channel))

    data_file = '/diff_1_minseed_3_z_0_finalgenes.csv'

    fake_counts = []
    real_counts = []
    threshs = []

    for thresh_num in np.arange(0,11):
        gene_calls = Table.read_table(data_dir.replace('{tnum}',str(thresh_num))+data_file)
        fake_count = gene_calls.where('genes', are.containing('fake')).num_rows
        real_count = gene_calls.num_rows -fake_count

        fake_counts.append(fake_count)
        real_counts.append(real_count)
        threshs.append(thresh_num)

    cdbk = Table.read_table(('$USER_ENT$notebook_pyfiles/codebooks_converted/channel_{CH}_converted.csv').replace('{CH}',str(channel)))
    real_codewords = cdbk.where('gene name', are.not_containing('fake')).num_rows
    fake_codewords = cdbk.where('gene name', are.containing('fake')).num_rows
    
    
    index = threshs
    FPR_lists.append((np.asarray(fake_counts)/fake_codewords)/(np.asarray(real_counts)/real_codewords))
    

FPR_lists = np.asarray(FPR_lists)

FPR_lists_new = [index]
[FPR_lists_new.append(i) for i in FPR_lists]
FPR_lists_new = np.asarray(FPR_lists_new).T

with open('thresh_check.txt', 'w') as f:
    for line in FPR_lists_new:
        f.write(','.join([str((i)) for i in line]) + '\n')
        
    f.close()

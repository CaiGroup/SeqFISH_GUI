import os
import numpy as np
import getpass 


def WRITE_FILE(filename,orig,new,savenam):
    long_dir =filename.split('/')
    cwd = '/'.join(long_dir[:len(long_dir)-1]) + '/'
    
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    
    
    new_lines = []
    for line in Lines:
        new_line = line
        for orig_i, new_i in zip(orig,new):
            if orig_i in line:
                new_line = new_line.replace(orig_i, new_i)
        new_lines.append(new_line)

    if savenam in os.listdir(cwd):
        os.system('rm -r '+cwd+savenam)
        
    file1 = open(cwd+savenam, 'w')
    file1.writelines(new_lines)
    file1.close()
    
def jobremover(jobid):
    job_ID = jobid[0].replace('Submitted batch job ', '').replace(' ', '')
    job_ID = str(int(job_ID))

    job_substrings =[i[:25] for i in os.popen('squeue -u '+getpass.getuser()).readlines()[1:]]
    job_substrings = [i.replace(' ', '') for i in job_substrings]

    for job_substring in job_substrings:
        #print(job_ID,job_substrings)
        if job_ID in job_substring:
            os.system('scancel ' + job_substring)

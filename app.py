import tkinter as tk
import os
import numpy as np
from tkinter.font import Font
from tkinter import ttk
#from helper import *
import time
import getpass

global jobID_O_dapialign,jobID_O_preprocessing
jobID_O_dapialign = None
jobID_O_preprocessing = None

import pexpect, time
import os
import time
import sys


from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

def get_queue():
    child.sendline('squeue -u '+username.get())
    child.expect("~]", timeout=10)

    str_outs = str(child.before).split('\\r\\n')
    #str_outs = np.asarray(str_outs)[['squeue -u' not in i for i in str_outs]]
    return ('\n').join([i for i in str_outs[1:len(str_outs)-1]])
    

def get_lisdir(directory):
    child.sendline('''python -c "import sys;import os; print(os.listdir('$dir$'))"'''.replace('$dir$', directory))
    child.expect("~]", timeout=10)

    filez = str(child.before).split('\\r\\n')[1].split('\\')

    filez = [i.replace("'", "") for i in np.asarray(filez)[[i!= "', " and i!= '[' and i!= ']' for i in filez]]]
    return filez[:len(filez)-1]
    
def clean_slurms(path):
    child.sendline("cd "+path)
    child.expect("]", timeout=10)
    
    run_command('rm slurm*')
    
    child.sendline("cd ")
    child.expect("~]", timeout=10)
    
def RUN_FILE(loc, filename):
    child.sendline("cd "+loc)
    child.expect("]", timeout=10)
    
    child.sendline("sbatch "+filename)
    child.expect("]", timeout=10)
        
    child.sendline("cd ")
    child.expect("~]", timeout=10)
    
def RUN_FILE_PY(loc, filename):
    child.sendline("cd "+loc)
    child.expect("]", timeout=10)
    
    child.sendline("/groups/CaiLab/personal/python_env/bin/python3 "+filename)
    child.expect("]", timeout=300)
    
    child.sendline("cd ")
    child.expect("~]", timeout=10)
    
    child.sendline(("cat seqFISH_DASH/thresh_check/thresh_check.txt"))
    child.expect("~]", timeout=50)
    lines = child.before
    lines = str(lines).split('\\r\\n')
    
    return lines[1:len(lines)-1]

def run_command(command):
    child.sendline(command)
    child.expect("]", timeout=10)
    
def get_grep(path):
    child.sendline('cd '+path)
    child.expect("]", timeout=10)

    child.sendline("grep -i error slurm*")
    child.expect("]", timeout=10)

    child.sendline('cd ')
    child.expect("~]", timeout=10)
    out_val = str(child.before).replace('grep -i error slurm*','')
    return out_val
    
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
    
    child.sendline('rm -r '+cwd+savenam)
    child.expect("~]", timeout=10)
    
    if 'batch' in savenam:
        child.sendline('cp '+ (cwd+ 'root.file ')+ (cwd+ savenam))
        child.expect("~]", timeout=10)
    
    for new_line in new_lines:
        child.sendline('echo -n "$line" >> $file'.replace('$file',cwd+savenam).replace('$line',new_line))
        child.expect("~]", timeout=10)
    
    
def jobremover(jobid):
    job_ID = str(int(jobid))
    job_substrings =[i[:25] for i in get_queue().split('\n')[1:]]
    job_substrings = [i.replace(' ', '') for i in job_substrings]
    for job_substring in job_substrings:
        #print(job_ID,job_substrings)
        if job_ID in job_substring:
            child.sendline('scancel ' + job_substring)
            child.expect("~]", timeout=10)
            
class login:
    def __init__(self, master):
        def printtext():
            print(user_ent.get())
        self.master = master
        
        self.canvas1 = tk.Canvas( self.master, width = 400,height = 400,bg='#df7039')
        self.canvas1.pack(fill = "both", expand = True)
        
        myFont = Font(family="liberation sans", size=24)
        self.canvas1.create_text( 200, 50, text = "Caltech",fill="#FFFFFF", font=('liberation sans', '32', 'bold italic'))
        self.canvas1.create_text( 100, 100,anchor = "nw", text = "Please sign-in below:",fill="#FFFFFF",font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 100, 125, anchor = "nw",text = "User-ID",fill="#FFFFFF",font=('liberation sans', '11', 'bold'))
        
        self.canvas1.create_text( 100, 195, anchor = "nw",text = "Password",fill="#FFFFFF",font=('liberation sans', '11', 'bold'))
    
                
        global username, password
        username= tk.Entry(self.canvas1, width= 22)
        username.focus_set()
        self.canvas1.create_window(200,160,window=username)
        
        password= tk.Entry(self.canvas1, width= 22, show='*')
        password.focus_set()
        self.canvas1.create_window(200,230,window=password)
        
        #user_ent.get()
        
        demo = tk.Button( self.master, text = "Sign-In",command = self.Demo1_W,highlightthickness = -2, bd = -2,borderwidth=-5) #
        
        dapi_align_canvas = self.canvas1.create_window( 200, 300,anchor = "nw",window = demo)
        
        self.master.mainloop()
        
    def close_window(self):
        self.master.destroy()
    def Demo1_W(self):
        try:
            global child
            child = pexpect.spawn(('ssh %USER%@login.hpc.caltech.edu').replace('%USER%',username.get()))
            child.logfile = open("mylog", "wb")
            child.expect("assword", timeout=20)
            child.sendline(password.get())
            
            child.expect('(1-1)', timeout=20)
            child.sendline('1')
            child.expect("~]", timeout=20)
            self.newWindow = tk.Toplevel(self.master)
            self.app = Demo1(self.newWindow)
            self.canvas1.create_text( 100, 270, anchor = "nw",text = "DUO Request Approved",fill="#81bd61",font=('liberation sans', '11', 'bold'))
        except:
            self.canvas1.create_text( 100, 270, anchor = "nw",text = "Log-In Failed",fill="#d62929",font=('liberation sans', '11', 'bold'))
class Demo1:
    def __init__(self, master):
        def printtext():
            print(user_ent.get())
        self.master = master
        
        canvas1 = tk.Canvas( self.master, width = 500,height = 486)
        canvas1.pack(fill = "both", expand = True)
        canvas1.create_image( 0,0, image = bg,anchor = "nw")
        myFont = Font(family="liberation sans", size=24)
        canvas1.create_text( 250, 480, text = "Image credit: NASA/JPL-Caltech/KPNO/University of Missouri-Kansas City",fill="#FFFFFF", font=('liberation sans', '8', 'bold italic'))
        #https://www.nasa.gov/jpl/spitzer/galaxy-cluster-pia17565
        
        canvas1.create_text( 250, 50, text = "SeqFISH DASH",fill="#FFFFFF", font=('liberation sans', '24', 'bold italic'))
        canvas1.create_text( 250, 125, text = "Welcome. Here you can serially run the SeqFISH\nDASH pipeline. Simply click on any of the buttons\nbelow to launch an interactive portal to run the\nSeqFISH DASH pipeline components.",fill="#FFFFFF",font=('liberation sans', '11', 'bold'))
        canvas1.create_text( 250, 200, text = "Raw Data Directory: \n(e.g. /central/groups/CaiLab/personal/$USER/raw/$EXP/)",fill="#FFFFFF",font=('liberation sans', '11', 'bold'))
        
        
        canvas1.create_text( 110, 300, text = "Pipeline Components",fill="#FFFFFF", font=('liberation sans', '11', 'bold'))
        canvas1.create_text( 400, 300, text = "Helper Tools",fill="#FFFFFF", font=('liberation sans', '11', 'bold'))
                
                
        global user_ent
        user_ent= tk.Entry(canvas1, width= 22)
        user_ent.insert(0, "/central/groups/CaiLab/personal/Michal/raw/2022-02-11_p4p5p7_Neuro1098_5_pool1/")
        user_ent.focus_set()
        canvas1.create_window(220,240,window=user_ent)
        
        
        
        #dapi_align = tk.Button( self.master, text = "Dapi-Align",command = self.DAPI_W,highlightthickness = -2, bd = -2,borderwidth=-5)
        #dapi_align_canvas = canvas1.create_window( 50, 320,anchor = "nw",window = dapi_align)
        
        preprocessing = tk.Button( self.master, text = "1. Pre-Process",command = self.Preprocess_W,highlightthickness = -2, bd = -2,borderwidth=-5,width= 10)
        preprocessing_canvas = canvas1.create_window( 50, 320,anchor = "nw",window = preprocessing)
                
        optimize = tk.Button( self.master, text = "2. Optimize",command = self.optimize_W,highlightthickness = -2, bd = -2,borderwidth=-5,width= 10)
        canvas1.create_window( 50, 365,anchor = "nw",window = optimize)
        
        check_preprocessing = tk.Button( self.master, text = "Check",command = self.check_preprocessing_W,highlightthickness = -2, bd = -2,borderwidth=-5,width= 5)
        canvas1.create_window( 215, 337,anchor = "nw",window = check_preprocessing)
        
        check_opt = tk.Button( self.master, text = "Check",command = self.check_OPT_W,highlightthickness = -2, bd = -2,borderwidth=-5,width= 5)
        canvas1.create_window( 215, 402,anchor = "nw",window = check_opt)
        
        postprocess = tk.Button( self.master, text = "3. Post-Process",command = self.postprocess_W,highlightthickness = -2, bd = -2,borderwidth=-5,width= 10)
        canvas1.create_window( 50, 410,anchor = "nw",window = postprocess)
        
        
        checkqueue = tk.Button( self.master, text = "Check Queue",command = self.checkqueue_W,highlightthickness = -2, bd = -2,borderwidth=-5)
        checkqueue_canvas = canvas1.create_window( 350, 320,anchor = "nw",window = checkqueue)
        
        
        checkerrors = tk.Button( self.master, text = "Check Errors",command = self.checkerrors_W,highlightthickness = -2, bd = -2,borderwidth=-5)
        checkerrors_canvas = canvas1.create_window( 350, 350,anchor = "nw",window = checkerrors)
        
        #self.master.mainloop()
        

    def DAPI_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = DAPI_W_C(self.newWindow)
        
    def optimize_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = optimize_W_C(self.newWindow)
        
    def Preprocess_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Preprocess_W_C(self.newWindow)
                        
    def check_OPT_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = check_OPT_W_C(self.newWindow)
        
    def check_preprocessing_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = check_preprocessing_W_C(self.newWindow)
    def postprocess_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = postprocess_W_C(self.newWindow)
        
    def checkqueue_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = checkqueue_W_C(self.newWindow)
    def checkerrors_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = checkerrors_W_C(self.newWindow)
        
class check_preprocessing_W_C:
    def __init__(self, master):
        self.master = master
        self.master.wm_title("Check Errors in Pre-Processing")
        self.canvas1 = tk.Canvas( self.master, width = 400,height = 100)
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 200, 50, text = "Coming Soon!",fill="#FF0000", font=('liberation sans', '12', 'bold'))
        
        
class check_OPT_W_C:
    def __init__(self, master):
        self.master = master
        #self.master.wm_title("Check Errors in Optimizaton")
        #self.canvas1 = tk.Canvas( self.master, width = 400,height = 100)
        #self.canvas1.pack(fill = "both", expand = True)
        #self.canvas1.create_text( 200, 50, text = "Coming Soon!",fill="#FF0000", font=('liberation sans', '12', 'bold'))
        
        decoded_lis = np.asarray(get_lisdir(user_ent.get() + 'notebook_pyfiles/decoded/' ))
        decoded_lis = decoded_lis[['OPT_CH' in i for i in decoded_lis]]
        decoded_lis = [str(i) for i in np.sort([int(i.replace('OPT_CH', '')) for i in decoded_lis])]
        decoded_lis = ','.join(decoded_lis)
        
        #
        filename = 'seqFISH_DASH/thresh_check/RUN_THRESH_CHECK_TEMPLATE.py'
        orig = ['$CHANNEL_NUM$','$USER_ENT$']
        new = [decoded_lis,user_ent.get() ]
        savenam = 'RUN_THRESH_CHECK.py'
        WRITE_FILE(filename,orig,new,savenam)
        
        lines = RUN_FILE_PY('seqFISH_DASH/thresh_check', 'RUN_THRESH_CHECK.py')
        lines = np.asarray([[float(j) for j in (i.split(','))] for i in lines])
        lines = lines.T
        
        #x = np.linspace(0, 2 * np.pi, 400)
        #y = np.sin(x ** 2)
        fig, axs = plt.subplots(lines.shape[0]-1)
        
        fig.suptitle('FPR Analysis Ch1-' + str(lines.shape[0]-1))
        for i in np.arange(1, lines.shape[0]):
            axs[i-1].scatter(lines[0], lines[i])
            for x,y,t in zip(lines[0], lines[i],lines[0]):
                axs[i-1].annotate(str(int(t)), (x,y),c='red')
                      
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,master = self.master)
        canvas.draw()
      
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
      
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,self.master)
        toolbar.update()
      
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
        #print(lines)
        #print((lines).shape)
        
class DAPI_W_C:
    def __init__(self, master):
        #try:
        self.master = master
        self.canvas1 = tk.Canvas( self.master, width = 500,height = 486)
        self.canvas1.create_image( 0,0, image = dapi,anchor = "nw")
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 250, 50, text = "DAPI Alignment",fill="#FFFFFF", font=('liberation sans', '24', 'bold italic'))

        filename = 'seqFISH_DASH/pre_processing/dapi_alignment_files/batch_dapi_TEMPLATE.py'
        orig = ['$FILENAME$']
        new = [('i').replace('i',user_ent.get())]
        savenam = 'batch_dapi.py'
        WRITE_FILE(filename,orig,new,savenam)

        hybes = np.asarray(get_lisdir(user_ent.get()))
        hyb = hybes[['Hyb' in i for i in hybes]][0]
        pos_nums = [int(i.replace('MMStack_Pos','').replace('.ome.tif','')) for i in get_lisdir(user_ent.get() +hyb)]
        hyb_nums = [int(i.replace('HybCycle_','')) for i in hybes[['Hyb' in i for i in hybes]]]

        self.canvas1.create_text( 250, 200, text = "Sucessfully read in "+ str(len(hyb_nums))+" hybe-cycles\n" +"in " + str(len(pos_nums)) + ' positions.',fill="#187509", font=('liberation sans', '12', 'bold'))
        
        filename = 'seqFISH_DASH/pre_processing/dapi_alignment_files/dapi_align_TEMPLATE.batch'
        orig = ['$POSRNG$']
        new = [str(min(pos_nums)) +'-'+str(max(pos_nums))]
        savenam = 'dapi_align.batch' 
        WRITE_FILE(filename,orig,new,savenam)

        run_dapi_align = tk.Button( self.master, text = "Run Alignment!",command = self.run_dapi_alignment,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 250, 320,anchor = "nw",window = run_dapi_align)
            
        
        #except:
        #    self.canvas1.create_text( 250, 200, text ='Cannot Read Directory Supplied! Check syntaxt.',fill="#820812", font=('liberation sans', '12', 'bold'))

            #print()

    def close_windows(self):
        self.master.destroy()
    def run_dapi_alignment(self):
        RUN_FILE('seqFISH_DASH/dapi_alignment_files/', 'dapi_align.batch')
        self.canvas1.create_text( 250, 400, text = "Jobs submitted!",fill="#187509", font=('liberation sans', '12', 'bold'))

class Preprocess_W_C:
    def __init__(self, master):
        child.sendline('cd')
        child.expect("~]", timeout=10)
        
        self.master = master
        self.canvas1 = tk.Canvas( self.master, width = 500,height = 486)
        self.canvas1.create_image( 0,0, image = preprocess_bkg_im,anchor = "nw")
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 485, 250, text = "Preprocessing",fill="#FFFFFF", font=('liberation sans', '24', 'bold italic'),angle=-90)
        
        global hybes
        hybes = np.asarray(get_lisdir(user_ent.get()))
        hybes = np.asarray(get_lisdir(user_ent.get()))
        hybes = hybes[['Hyb' in i for i in hybes]]
        hyb = hybes[0]
        global pos_nums_preprocessing
        pos_nums_preprocessing = [int(i.replace('MMStack_Pos','').replace('.ome.tif','')) for i in get_lisdir(user_ent.get() +hyb)]
        pos_nums_preprocessing = [int(i.replace('HybCycle_','')) for i in hybes[['Hyb' in i for i in hybes]]]
        hyb_num = len(hybes)
        pos_num = len(pos_nums_preprocessing)
        
        self.canvas1.create_text( 250, 30, text = "Sucessfully read in "+ str(len(hybes))+" hybe-cycles\n" +"in " + str(len(pos_nums_preprocessing)) + ' positions.',fill="#187509", font=('liberation sans', '12', 'bold'))
            
        self.canvas1.create_text( 100, 75, text = "Image Dimension Along One Axis (eg. 2048):",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
        global preprocess_dim
        preprocess_dim= tk.Entry(self.canvas1, width= 10)
        preprocess_dim.insert(0, "2048")
        preprocess_dim.focus_set()
        self.canvas1.create_window(100,95,window=preprocess_dim,anchor = "nw")
        
        global channels_to_opt_preprocess
        data=['1','2','3','4','5']
        channels_to_opt_preprocess = tk.StringVar()
        channels_to_opt_preprocess.set('3')
        p = tk.OptionMenu(self.master, channels_to_opt_preprocess, *data)
        self.canvas1.create_window(100,170,window=p,anchor = "nw")
        self.canvas1.create_text( 100, 150, text = "Total # of Channels:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
        
        global barcoding_rounds
        data=['1','2','3','4','5', '6', '7', '8']
        barcoding_rounds = tk.StringVar()
        barcoding_rounds.set('4')
        barcoding_rounds_menu = tk.OptionMenu(self.master, barcoding_rounds, *data)
        self.canvas1.create_window(250,170,window=barcoding_rounds_menu,anchor = "nw")
        self.canvas1.create_text( 250, 150, text = "Total # of Barcoding Rounds:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
        
        self.canvas1.create_text( 100, 220, text = "Path to Codebooks:\n(leave blank if you previously converted codebooks) ",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
        global codebook_path
        codebook_path= tk.Entry(self.canvas1, width= 10)
        codebook_path.focus_set()
        self.canvas1.create_window(100,255,window=codebook_path,anchor = "nw")
        self.canvas1.create_text( 100, 290, text = "Path Convention: /central/.../codebooks/\n\nCodebook Naming Convention: channel_{NUM}.csv \nwhere {NUM} is an integer (eg. channel_1.csv). The \nfirst channel must have a {NUM} = 1, and so on for \nthe other channels.",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
        
        
        #self.canvas1.create_text( 250, 120, text ='Dapi Alignment Complete!',fill="#187509", font=('liberation sans', '12', 'bold'))
        run_prep = tk.Button( self.master, text = "Run Pre-Processing",command = self.run_preprocessing,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window(250, 370,anchor = "nw",window = run_prep)
        #except:
        #    self.canvas1.create_text( 250, 200, text ='Cannot Read Directory Supplied! Check syntaxt.',fill="#820812", font=('liberation sans', '12', 'bold'))

    def close_windows(self):
        self.master.destroy()
    def run_preprocessing(self):
        filename = 'seqFISH_DASH/pre_processing/preprocessing_files/batch_correct_TEMPLATE.py'
        orig = ['$FILENAME$', '$DIMENSION$']
        new = [user_ent.get() + 'notebook_pyfiles/dapi_aligned/', str(preprocess_dim.get())]
        savenam = 'batch_correct.py'
        WRITE_FILE(filename,orig,new,savenam)


        filename = 'seqFISH_DASH/pre_processing/preprocessing_files/correct_many_TEMPLATE.batch'
        orig = ['$POSRNG$']
        new = [str(min(pos_nums_preprocessing)) +'-'+str(max(pos_nums_preprocessing))]
        savenam = 'correct_many.batch'
        WRITE_FILE(filename,orig,new,savenam)
        
        
        
        filename = 'seqFISH_DASH/pre_processing/dapi_alignment_files/batch_dapi_TEMPLATE.py'
        orig = ['$FILENAME$']
        new = [('i').replace('i',user_ent.get())]
        savenam = 'batch_dapi.py'
        WRITE_FILE(filename,orig,new,savenam)
        
        
        filename = 'seqFISH_DASH/pre_processing/dapi_alignment_files/dapi_align_TEMPLATE.batch'
        orig = ['$POSRNG$']
        new = [str(min(pos_nums_preprocessing)) +'-'+str(max(pos_nums_preprocessing))]
        savenam = 'dapi_align.batch'
        WRITE_FILE(filename,orig,new,savenam)
        
        print(channels_to_opt_preprocess.get())
        print(codebook_path.get())
        make_codebooks = 'True'
        if codebook_path.get() == '':
            make_codebooks = 'False'
                
        filename = 'seqFISH_DASH/pre_processing/run_pre_TEMPLATE.py'
        orig = ['$DATA_DIR$', '$PATH_USER$','$MAKE_CODEBOOKS$', '$CHANNELNUM$', '$HYB_COUNT$', '$Barcode_COUNT$']
        new = [user_ent.get(), codebook_path.get(),make_codebooks, str(int(channels_to_opt_preprocess.get())+1), str(len(hybes)), barcoding_rounds.get()]
        savenam = 'run_pre.py'
        WRITE_FILE(filename,orig,new,savenam)
        
        RUN_FILE('seqFISH_DASH/pre_processing', 'run_pre.batch')
        
        self.canvas1.create_text( 250, 400, text = "Jobs submitted!",fill="#187509", font=('liberation sans', '12', 'bold'))
        
class optimize_W_C:
    def __init__(self, master):
        child.sendline('cd')
        child.expect("~]", timeout=10)
        self.master = master
        self.canvas1 = tk.Canvas( self.master, width = 500,height = 486)
        self.canvas1.create_image( 0,0, image = optimize_bkg_im,anchor = "nw")
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 485, 250, text = "Optimize Dot Detection",fill="#FFFFFF", font=('liberation sans', '24', 'bold italic'),angle=-90)

        #try:

        hybes = np.asarray(get_lisdir(user_ent.get()))
        hyb = hybes[['Hyb' in i for i in hybes]][0]
        global pos_nums
        pos_nums = [int(i.replace('MMStack_Pos','').replace('.ome.tif','')) for i in get_lisdir(user_ent.get() +hyb)]
        hyb_nums = [int(i.replace('HybCycle_','')) for i in hybes[['Hyb' in i for i in hybes]]]
        hyb_num = len(hyb_nums)
        pos_num = len(pos_nums)

        path_dapi_aligned_files = user_ent.get() + 'notebook_pyfiles/pre_processed_images/'
        
        global hybes_pre_processed
        hybes_pre_processed = get_lisdir(path_dapi_aligned_files)
        hybes_pre_processed =  np.asarray(hybes_pre_processed)[['Hyb' in i for i in hybes_pre_processed]]
        hybes_pre_processed = hybes_pre_processed[np.argsort([int(i.replace('HybCycle_','')) for i in hybes_pre_processed])]
        pos_lens = list(set([len(get_lisdir(path_dapi_aligned_files + i)) for i in hybes_pre_processed]))

        if len(pos_lens) !=1 or pos_lens[0] != pos_num or len(hybes_pre_processed) != hyb_num:
            self.canvas1.create_text( 250, 200, text ='Pre-processing Incomplete or Failed!',fill="#820812", font=('liberation sans', '12', 'bold'))
        else:
            self.canvas1.create_text( 250, 20, text ='Pre-processing Complete!',fill="#187509", font=('liberation sans', '12', 'bold'))
            
            global channels_to_opt
            data=['1','2','3','4','5']
            channels_to_opt = tk.StringVar()
            channels_to_opt.set('3')
            p = tk.OptionMenu(self.master, channels_to_opt, *data)
            self.canvas1.create_window(100,100,window=p,anchor = "nw")
            self.canvas1.create_text( 100, 80, text = "Number of Channels to Analyze:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
            
            
            self.canvas1.create_text( 100, 140, text = "Hyb Offset (leave 0 if your first hyb is labeled HybCycle_0):",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
            global hyboffset
            hyboffset= tk.Entry(self.canvas1, width= 5)
            hyboffset.insert(0, "0")
            hyboffset.focus_set()
            self.canvas1.create_window(100,160,window=hyboffset,anchor='nw')
            
            
            global pos_to_opt, all_positions_preprocessed
            all_positions_preprocessed=np.sort([int(i.replace('MMStack_Pos','').replace('.ome.tif','') ) for i in get_lisdir(path_dapi_aligned_files + hybes_pre_processed[0])])
            all_positions_preprocessed = [str(i) for i in all_positions_preprocessed]
            all_positions_preprocessed = all_positions_preprocessed[1:(len(all_positions_preprocessed)-1)]
            pos_to_opt = tk.StringVar()
            pos_to_opt.set('1')
            self.canvas1.create_window(100,230,window=tk.OptionMenu(self.master, pos_to_opt, *all_positions_preprocessed),anchor = "nw")
            self.canvas1.create_text( 100, 200, text = "Position to use for Optimization\n(neigboring two positions are included):",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
            
            self.canvas1.create_text( 100, 270, text = "DAOStarFinder Absolute Minimum Threshold:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
            global threshold_min
            threshold_min= tk.Entry(self.canvas1, width= 5)
            threshold_min.insert(0, "2")
            threshold_min.focus_set()
            self.canvas1.create_window(100,290,window=threshold_min,anchor='nw')
            
            self.canvas1.create_text( 100, 330, text = "DAOStarFinder Absolute Maximum Threshold:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
            global threshold_max
            threshold_max= tk.Entry(self.canvas1, width= 5)
            threshold_max.insert(0, "10")
            threshold_max.focus_set()
            self.canvas1.create_window(100,350,window=threshold_max,anchor='nw')
            
            
        
            self.run = tk.Button(self.master, text = 'Run', width =4, command = self.RUN_F,highlightthickness = -2, bd = -2,borderwidth=-5)
            self.canvas1.create_window( 350, 380,anchor = "nw",window = self.run)
            
            
        #except:
        #    self.canvas1.create_text( 250, 200, text ='Cannot Read Directory Supplied! Check syntaxt.',fill="#820812", font=('liberation sans', '12', 'bold'))
    def RUN_F(self):
            if int(hyboffset.get()) != 0:
                print('Decrease hyb nums by ' +str(int(hyboffset.get())))
                
                child.sendline("cd "+user_ent.get() + 'notebook_pyfiles/pre_processed_images/')
                child.expect("]", timeout=10)
            
                for old_hyb in hybes_pre_processed:
                    new_hyb = 'HybCycle_' + str(int(old_hyb.replace('HybCycle_','')) - int(hyboffset.get()))
                    run_command('mv ohyb nhyb'.replace('ohyb', old_hyb).replace('nhyb', new_hyb))
            
                child.sendline("cd ")
                child.expect("~]", timeout=10)
                    
            filename = 'seqFISH_DASH/optimization_files/run_op_TEMPLATE.py'
            orig = ['#USERINPUT#','#CHANNELNUM#','#HYB_START#','#HYB_END#','#NUM_HYB#','#CENTPOS#']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1), '0', str(len(hybes_pre_processed)-1), str(len(hybes_pre_processed)),pos_to_opt.get()]
            savenam = 'run_op.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            ##################################################################################################################################
            
            filename = 'seqFISH_DASH/optimization_files/dot_detection_files/find_thresh_individual_TEMPLATE.batch'
            orig = ['$HYBRNG$']
            new = ['0-'+str(len(hybes_pre_processed)-1)]
            savenam = 'find_thresh_individual.batch'
            WRITE_FILE(filename,orig,new,savenam)
            
            index_to_opt = np.arange(1,len(all_positions_preprocessed)+1)[pos_to_opt.get() == np.asarray(all_positions_preprocessed)][0]
            filename = 'seqFISH_DASH/optimization_files/dot_detection_files/batch_thresh_individual_TEMPLATE.py'
            orig = ['$USERINPUT$','$CHANNELNUM$','$POS_1$','$POS_2$','$POS_3$', '$POS_START$', '$POS_STOP$','$threshold_min$','$threshold_max$']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1), str(index_to_opt-1),str(index_to_opt),str(index_to_opt+1),str(int(pos_to_opt.get())-1), str(int(pos_to_opt.get())+2), threshold_min.get(), threshold_max.get()]
            savenam = 'batch_thresh_individual.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            
            ##################################################################################################################################
            
            filename = 'seqFISH_DASH/optimization_files/dot_detection_files/dotdetection_individual_opt_TEMPLATE.batch'
            orig = ['$HYBRNG$']
            new = ['0-'+str(len(hybes_pre_processed)-1)]
            savenam = 'dotdetection_individual_opt.batch'
            WRITE_FILE(filename,orig,new,savenam)
            
            filename = 'seqFISH_DASH/optimization_files/dot_detection_files/batch_dotdetection_individual_opt_TEMPLATE.py'
            orig = ['$USERINPUT$','$CENTPOS$','$CHANNELNUM$','$POS_START$','$POS_STOP$','$HYBTOT$']
            new = [user_ent.get(),pos_to_opt.get(),str(int(channels_to_opt.get())+1),str(int(pos_to_opt.get())-1), str(int(pos_to_opt.get())+2),str(len(hybes_pre_processed))]
            savenam = 'batch_dotdetection_individual_opt.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            ###########################
            
            filename = 'seqFISH_DASH/optimization_files/decoding_files/dash_radial_decoding_batch_BEFORE_OP_TEMPLATE.py'
            orig = ['$USERENT$','$CHANNELNUM$', '$POSNUM$', '$HYBTOT$','$Barcode_COUNT$']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1), pos_to_opt.get(),str(len(hybes_pre_processed)), barcoding_rounds.get()]
            savenam = 'dash_radial_decoding_batch_BEFORE_OP.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            
            filename = 'seqFISH_DASH/optimization_files/decoding_files/dash_radial_decoding_BEFORE_OP_TEMPLATE.batch'
            orig = []
            new = []
            savenam = 'dash_radial_decoding_BEFORE_OP.batch'
            WRITE_FILE(filename,orig,new,savenam)
            
            RUN_FILE('seqFISH_DASH/optimization_files/', 'run_op.batch')
            
            
class postprocess_W_C:
    def __init__(self, master):
        child.sendline('cd')
        child.expect("~]", timeout=10)
        self.master = master
        self.canvas1 = tk.Canvas( self.master, width = 500,height = 486)
        self.canvas1.create_image( 0,0, image = post_bkg_im,anchor = "nw")
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 485, 250, text = "Dot Detection + Decoding",fill="#FFFFFF", font=('liberation sans', '24', 'bold italic'),angle=-90)

        #try:

        hybes = np.asarray(get_lisdir(user_ent.get()))
        hyb = hybes[['Hyb' in i for i in hybes]][0]
        global pos_nums
        pos_nums = [int(i.replace('MMStack_Pos','').replace('.ome.tif','')) for i in get_lisdir(user_ent.get() +hyb)]
        hyb_nums = [int(i.replace('HybCycle_','')) for i in hybes[['Hyb' in i for i in hybes]]]
        hyb_num = len(hyb_nums)
        pos_num = len(pos_nums)

        path_dapi_aligned_files = user_ent.get() + 'notebook_pyfiles/pre_processed_images/'
        
        global hybes_pre_processed, pos_lens
        hybes_pre_processed = get_lisdir(path_dapi_aligned_files)
        hybes_pre_processed =  np.asarray(hybes_pre_processed)[['Hyb' in i for i in hybes_pre_processed]]
        hybes_pre_processed = hybes_pre_processed[np.argsort([int(i.replace('HybCycle_','')) for i in hybes_pre_processed])]
        pos_lens = list(set([len(get_lisdir(path_dapi_aligned_files + i)) for i in hybes_pre_processed]))
        
        global opt_present
        decoded_present = 'decoded' in np.asarray(get_lisdir(user_ent.get()+'notebook_pyfiles'))

        if len(pos_lens) !=1 or pos_lens[0] != pos_num or len(hybes_pre_processed) != hyb_num:
            self.canvas1.create_text( 250, 200, text ='Pre-processing Incomplete or Failed!',fill="#820812", font=('liberation sans', '12', 'bold'))
        else:
            self.canvas1.create_text( 250, 20, text ='Pre-processing Complete!',fill="#187509", font=('liberation sans', '12', 'bold'))
                
            if decoded_present:
                self.canvas1.create_text( 250, 35, text ='Optimization Appears Complete!',fill="#187509", font=('liberation sans', '12', 'bold'))
                
                global channels_to_opt
                data=['1','2','3','4','5']
                channels_to_opt = tk.StringVar()
                channels_to_opt.set('3')
                p = tk.OptionMenu(self.master, channels_to_opt, *data)
                self.canvas1.create_window(100,100,window=p,anchor = "nw")
                self.canvas1.create_text( 100, 80, text = "Number of Channels to Analyze:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
                
                self.canvas1.create_text( 100, 140, text = "Optimal Threshold Set (comma separated) [Ex: 10,10,9]:",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
                global thresh_opt
                thresh_opt= tk.Entry(self.canvas1, width= 10)
                thresh_opt.insert(0, "10,10,10")
                thresh_opt.focus_set()
                self.canvas1.create_window(100,160,window=thresh_opt,anchor='nw')
                
                
                global pos_to_opt, all_positions_preprocessed
                all_positions_preprocessed=np.sort([int(i.replace('MMStack_Pos','').replace('.ome.tif','') ) for i in get_lisdir(path_dapi_aligned_files + hybes_pre_processed[0])])
                all_positions_preprocessed = [str(i) for i in all_positions_preprocessed]
                all_positions_preprocessed = all_positions_preprocessed[1:(len(all_positions_preprocessed)-1)]
                pos_to_opt = tk.StringVar()
                pos_to_opt.set('1')
                self.canvas1.create_window(100,230,window=tk.OptionMenu(self.master, pos_to_opt, *all_positions_preprocessed),anchor = "nw")
                self.canvas1.create_text( 100, 200, text = "Position Used for Optimization\n(reference to optimization):",fill="#FFFFFF",anchor = "nw",font=('liberation sans', '11', 'bold'))
                
                
                
            
                self.run = tk.Button(self.master, text = 'Run', width =4, command = self.RUN_F,highlightthickness = -2, bd = -2,borderwidth=-5)
                self.canvas1.create_window( 350, 380,anchor = "nw",window = self.run)
            
            
        #except:
        #    self.canvas1.create_text( 250, 200, text ='Cannot Read Directory Supplied! Check syntaxt.',fill="#820812", font=('liberation sans', '12', 'bold'))
    def RUN_F(self):
                    
            filename = 'seqFISH_DASH/post_processing/run_post_TEMPLATE.py'
            orig = ['#USERINPUT#','#CHANNELNUM#','#HYB_START#','#HYB_END#','#NUM_HYB#','#POSNUM#']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1), '0', str(len(hybes_pre_processed)-1), str(len(hybes_pre_processed)),str(pos_lens[0])]
            savenam = 'run_post.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            ##################################################################################################################################
            
            filename = 'seqFISH_DASH/post_processing/dot_detection_files/dotdetection_individual_TEMPLATE.batch'
            orig = ['$POSRNG$']
            new = ['0-'+str(int(pos_lens[0])-1)]
            savenam = 'dotdetection_individual.batch'
            WRITE_FILE(filename,orig,new,savenam)
            
            
            index_to_opt = np.arange(1,len(all_positions_preprocessed)+1)[pos_to_opt.get() == np.asarray(all_positions_preprocessed)][0]
            filename = 'seqFISH_DASH/post_processing/dot_detection_files/batch_dotdetection_individual_TEMPLATE.py'
            orig = ['$USERINPUT$','$CHANNELNUM$','$POS_START$', '$POS_STOP$','$THRESHLIST$','$NUM_HYB$']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1),str(int(pos_to_opt.get())-1), str(int(pos_to_opt.get())+2),thresh_opt.get() ,str(len(hybes_pre_processed))]
            savenam = 'batch_dotdetection_individual.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            
            ##################################################################################################################################
            
            filename = 'seqFISH_DASH/post_processing/decoding_files/dash_radial_decoding_batch_AFTER_OPTIMIZATION_TEMPLATE.py'
            orig = ['$USERENT$','$CHANNELNUM$', '$HYBTOT$']
            new = [user_ent.get(),str(int(channels_to_opt.get())+1), str(len(hybes_pre_processed))]
            savenam = 'dash_radial_decoding_batch_AFTER_OPTIMIZATION.py'
            WRITE_FILE(filename,orig,new,savenam)
            
            
            filename = 'seqFISH_DASH/post_processing/decoding_files/dash_radial_decoding_AFTER_OPTIMIZATION_TEMPLATE.batch'
            orig = ['$POSRNG$']
            new = ['0-'+str(pos_lens[0]-1)]
            savenam = 'dash_radial_decoding_AFTER_OPTIMIZATION.batch'
            WRITE_FILE(filename,orig,new,savenam)
            
            RUN_FILE('seqFISH_DASH/post_processing/', 'run_post.batch')
        
class checkqueue_W_C:
    def __init__(self, master):
        self.master = master
        #self.frame = tk.Frame(self.master)
        
        self.canvas1 = tk.Canvas( self.master, width = 300,height = 486,bg='#03102b')
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 10, 50, anchor='nw',text = get_queue(),fill="#FFD700", font=('liberation sans', '6', 'normal'))
        
        self.master.wm_title("Check Queue")
        #self.master.geometry("320x200")
        self.reloadbutton = tk.Button(self.master, text = 'Reload', width = 6, command = self.RELOAD,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 375,window = self.reloadbutton)
        
        self.cancelbutton = tk.Button(self.master, text = 'Cancel All GUI Jobs', width = 12, command = self.CANCEL,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 460,window = self.cancelbutton)
        
        self.removeslurmbutton = tk.Button(self.master, text = 'Remove Slurm Outs', width = 12, command = self.REMOVE_FILES,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 425,window = self.removeslurmbutton)
        
        #self.quitButton.pack()
        #self.frame.pack()
    def RELOAD(self):
        self.canvas1.delete("all")
        self.canvas1.pack(fill = "both", expand = True)
        
        self.canvas1.create_text( 10, 50, anchor='nw',text = get_queue(),fill="#FFD700", font=('liberation sans', '6', 'normal'))
        self.master.wm_title("Check Queue")
        #self.master.geometry("320x200")
        self.reloadbutton = tk.Button(self.master, text = 'Reload', width = 6, command = self.RELOAD,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 375,window = self.reloadbutton)
        
        self.cancelbutton = tk.Button(self.master, text = 'Cancel All GUI Jobs', width = 12, command = self.CANCEL,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 460,window = self.cancelbutton)
        
        self.removeslurmbutton = tk.Button(self.master, text = 'Remove Slurm Outs', width = 12, command = self.REMOVE_FILES,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 150, 425,window = self.removeslurmbutton)
        #self.master.destroy()
        
    def CANCEL(self):
        logfile = open('mylog', 'r')
        loglines = logfile.readlines()
        logfile.close()
        
        jobids = [int(i.replace('\n', '').replace('Submitted batch job ', '')) for i in np.asarray(loglines)[['Submitted batch job ' in i for i in loglines]]]
        [jobremover(i) for i in jobids]
        
        self.canvas1.delete("all")
        self.canvas1.pack(fill = "both", expand = True)
        self.canvas1.create_text( 70, 50, anchor='nw',text = get_queue(),fill="#FFD700", font=('liberation sans', '8', 'normal'))
        self.master.wm_title("Check Queue")
        #self.master.geometry("320x200")
        self.reloadbutton = tk.Button(self.master, text = 'Reload', width = 12, command = self.RELOAD,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 200, 380,anchor = "nw",window = self.reloadbutton)
        
        self.cancelbutton = tk.Button(self.master, text = 'Cancel All GUI Jobs', width = 12, command = self.CANCEL,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 200, 420,anchor = "nw",window = self.cancelbutton)
        
        self.removeslurmbutton = tk.Button(self.master, text = 'Remove Slurm Outs', width = 12, command = self.REMOVE_FILES,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 50, 400,anchor = "nw",window = self.removeslurmbutton)
    def REMOVE_FILES(self):
        clean_slurms('seqFISH_DASH/pre_processing/dapi_alignment_files')
        clean_slurms('seqFISH_DASH/pre_processing/preprocessing_files')
        
        clean_slurms('seqFISH_DASH/optimization_files/dot_detection_files')
        clean_slurms('seqFISH_DASH/optimization_files/decoding_files')
        #clean_slurms('seqFISH_DASH/optimization_files')
        
        
        clean_slurms('seqFISH_DASH/post_processing/dot_detection_files')
        clean_slurms('seqFISH_DASH/post_processing/decoding_files')
        #clean_slurms('seqFISH_DASH/post_processing')


        #sys.exit()
                  
class checkerrors_W_C:
    def __init__(self, master):
        self.master = master
        #self.frame = tk.Frame(self.master)
        self.canvas1 = tk.Canvas( self.master, width = 300,height = 486,bg='#03102b')
        self.canvas1.pack(fill = "both", expand = True)        
        self.master.wm_title("Check Errors")
        
        self.canvas1.create_text( 25, 100, anchor = "nw",text = "Errors in Dapi-Alignment:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 150,anchor = "nw", text = "Errors in Pre-Processing:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 200,anchor = "nw", text = "Errors in Optimization:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 250, anchor = "nw",text = "Errors in Dot-Detection:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 300,anchor = "nw", text = "Errors in Decoding:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        
        
        
        self.canvas1.create_image(200,100-6, anchor='nw', image=self.check_errors('seqFISH_DASH/pre_processing/dapi_alignment_files'))
        self.canvas1.create_image(200,150-6, anchor='nw', image=self.check_errors('seqFISH_DASH/pre_processing/preprocessing_files'))
        
        self.canvas1.create_image(200,200-6, anchor='nw', image=self.check_errors('seqFISH_DASH/optimization_files/dot_detection_files'))
        self.canvas1.create_image(250,200-6, anchor='nw', image=self.check_errors('seqFISH_DASH/optimization_files/decoding_files'))
        
        self.canvas1.create_image(200,250-6, anchor='nw', image=self.check_errors('seqFISH_DASH/post_processing/dot_detection_files'))
        self.canvas1.create_image(200,300-6, anchor='nw', image=self.check_errors('seqFISH_DASH/post_processing/decoding_files'))
        
        
        
        #'seqFISH_DASH/dapi_alignment_files', 'seqFISH_DASH/preprocessing_files', 'seqFISH_DASH/optimization_files/dot_detection_files',
        #'seqFISH_DASH/optimization_files/decoding_files', 'seqFISH_DASH/dot_detection_files', 'seqFISH_DASH/decoding_files'
        reload_button = tk.Button( self.master, text = "Reload",command = self.RELOAD,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 100, 375,anchor = "nw",window = reload_button)
        
        key_button = tk.Button( self.master, text = "Key",command = self.Error_Key_W,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 100, 425,anchor = "nw",window = key_button)
        
    def Error_Key_W(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = checkerrors_key_W_C(self.newWindow)
        
    def RELOAD(self):
        self.canvas1.delete("all")
        self.canvas1.pack(fill = "both", expand = True)
        self.master.wm_title("Check Errors")
        
        self.canvas1.create_text( 25, 100, anchor = "nw",text = "Errors in Dapi-Alignment:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 150,anchor = "nw", text = "Errors in Pre-Processing:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 200,anchor = "nw", text = "Errors in Optimization:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 250, anchor = "nw",text = "Errors in Dot-Detection:",fill="#FFD700", font=('liberation sans', '11', 'bold'))
        self.canvas1.create_text( 25, 300,anchor = "nw", text = "Errors in Decoding:",fill="#FFD700", font=('liberation sans', '11', 'bold'))



        self.canvas1.create_image(200,100-6, anchor='nw', image=self.check_errors('seqFISH_DASH/pre_processing/dapi_alignment_files'))
        self.canvas1.create_image(200,150-6, anchor='nw', image=self.check_errors('seqFISH_DASH/pre_processing/preprocessing_files'))

        self.canvas1.create_image(200,200-6, anchor='nw', image=self.check_errors('seqFISH_DASH/optimization_files/dot_detection_files'))
        self.canvas1.create_image(250,200-6, anchor='nw', image=self.check_errors('seqFISH_DASH/optimization_files/decoding_files'))

        self.canvas1.create_image(200,250-6, anchor='nw', image=self.check_errors('seqFISH_DASH/post_processing/dot_detection_files'))
        self.canvas1.create_image(200,300-6, anchor='nw', image=self.check_errors('seqFISH_DASH/post_processing/decoding_files'))



        #'seqFISH_DASH/dapi_alignment_files', 'seqFISH_DASH/preprocessing_files', 'seqFISH_DASH/optimization_files/dot_detection_files',
        #'seqFISH_DASH/optimization_files/decoding_files', 'seqFISH_DASH/dot_detection_files', 'seqFISH_DASH/decoding_files'
        reload_button = tk.Button( self.master, text = "Reload",command = self.RELOAD,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 100, 375,anchor = "nw",window = reload_button)

        key_button = tk.Button( self.master, text = "Key",command = self.Error_Key_W,highlightthickness = -2, bd = -2,borderwidth=-5)
        self.canvas1.create_window( 100, 425,anchor = "nw",window = key_button)

            
    def check_errors(self, path):
        if 'slurm' not in ' '.join(get_lisdir(path)):
            return yellow_c
        else:
            grepcheck = get_grep(path).lower()

            if 'error' in grepcheck:
                return red_c
            else:
                return green_c
class checkerrors_key_W_C:
    def __init__(self, master):
        self.master = master
        #self.frame = tk.Frame(self.master)
        self.canvas1 = tk.Canvas( self.master, width = 400,height = 200,bg='#02290d')
        self.canvas1.pack(fill = "both", expand = True)        
        self.master.wm_title("Check Errors - Key")
        
        self.canvas1.create_image(75,50-6, anchor='nw', image=green_c)
        self.canvas1.create_text( 125, 50, anchor = "nw",text = "= Slurm Output Present, No Errors",fill="#FFFFFF", font=('liberation sans', '11', 'bold'))
        
        self.canvas1.create_image(75,100-6, anchor='nw', image=yellow_c)
        self.canvas1.create_text( 125, 100, anchor = "nw",text = "= No Slurm Output Present",fill="#FFFFFF", font=('liberation sans', '11', 'bold'))
        
        self.canvas1.create_image(75,150-6, anchor='nw', image=red_c)
        self.canvas1.create_text( 125, 150, anchor = "nw",text = "= Slurm Error Present",fill="#FFFFFF", font=('liberation sans', '11', 'bold'))
            
def main():
    root = tk.Tk()
    root.option_add("*Label.Font", "helvetica 20 bold")

    
    #Load Background Images
    global bg, dapi,preprocess_bkg_im,optimize_bkg_im, post_bkg_im
    bg = tk.PhotoImage( file = "resources/bkg-new.png")
    dapi = tk.PhotoImage( file = "resources/dapi_im.png")
    preprocess_bkg_im = tk.PhotoImage( file = "resources/prep.png")
    optimize_bkg_im = tk.PhotoImage( file = "resources/optimize.png")
    post_bkg_im =tk.PhotoImage( file = "resources/post.png")
    
    global green_c,red_c, yellow_c
    green_c = tk.PhotoImage(file = "resources/green-circle.png")
    red_c = tk.PhotoImage(file = "resources/red-circle.png")
    yellow_c = tk.PhotoImage(file = "resources/yellow-circle.png")
    

    #root.wait_visibility(root)
    #root.wm_attributes('-alpha',0.6)
    root.wm_title("SeqFISH DASH")
    
    
    app = login(root)
    #root.mainloop()

if __name__ == '__main__':
    main()

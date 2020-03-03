import sys, os, shutil
import pandas as pd
import random
import csv
import itertools
import sox
import numpy as np
import pympi
from utils.py import *

"""

"""
#check if DiViMe repository pulled
import importlib
divime_loader = importlib.find_loader('DiViMe')
found = divime_loader is not None


def create_all_type_eaf(folder,output_dir,onset_function,skip):
    """
    Create eaf files from wav files, in random onset choice
    Args: 
        folder:a folder which contains wav files to proccess
        onset_function: chosen onset_function for random, periodic or HV eaf files
    Returns: a folder which contains eafs for each wav file of input filder
    """


    os.makedirs(os.path.dirname(output_dir), exist_ok=True)
    record_list = []
 
    for dirpath, dirnames, wavfiles in os.walk(folder): #getting into folder for proccessing files
        files= [f for f in wavfiles if f.endswith(".wav")] #exclude Ds.store
        for f in files:
            duration=sox.file_info.duration(dirpath+'/'+f) #get duration by path to file
            record_list.append([f.split('.')[0],dirpath+'/'+f,duration]) #list[file_id, file, file_duration]
        
    for record in record_list:
        # choose regions (5 by default)
        timestamps = onset_function(int(record[2]),skip) #onset fix, should be generic for every type of eaf
        timestamps = [(x * 60000, y * 60000) for x, y in timestamps]
        timestamps.sort(key=lambda tup: tup[0])

        # retrieve right age templates
        etf_path, pfsx_path = choose_template()

        # create
        print("making the eaf file")
        create_eaf(etf_path,record[0]+str(onset_function).split('_')[-1], output_dir, timestamps)
        shutil.copy(pfsx_path, os.path.join(os.path.dirname(output_dir), "{}.pfsx".format(record[0]+str(onset_function).split('_')[-1])))
        selected=create_output_csv(record[0], timestamps)
    #selected[['clip_num', 'onset', 'offset']] = selected[['clip_num', 'onset', 'offset']].astype(int)
    #selected.to_csv(os.path.join(output_dir,'selected_regions.csv'), index=False)
import sys, os, shutil
import pandas as pd
import random
import csv
import itertools
import sox
import numpy as np
import pympi
from utils import choose_onsets_periodic, choose_onsets_random,create_eaf,create_output_csv,choose_template


"""
Creates a generic eaf, proper both to random and periodic method
"""


def create_all_type_eaf(folder,output_dir,onset_function,eaf_type,t,*args):
    """
    Create eaf files from wav files, in random onset choice
    Args: 
        folder:a folder which contains wav files to proccess
        onset_function: chosen onset_function for random, periodic or HV eaf files
        eaf_type: random / periodic
        *args: for being able to call different arguments for periodic and random methods
    Returns: 
        output_dir:a folder which contains eafs for each wav file of input filder
    """


    os.makedirs(output_dir, exist_ok=True)
    record_list = []
 
    for dirpath, dirnames, wavfiles in os.walk(folder): #getting into folder for proccessing files
        files= [f for f in wavfiles if f.endswith(".wav")] #exclude Ds.store
        for f in files:
            duration=sox.file_info.duration(dirpath+'/'+f) #get duration by path to file
            record_list.append([f.split('.')[0],dirpath+'/'+f,duration]) #list[file_id, file, file_duration]
        
    for record in record_list:
        # choose regions (5 by default)
        timestamps = onset_function(int(record[2]),args,t) #onset fix, should be generic for every type of eaf
        timestamps = [(x * 10000, y * 10000) for x, y in timestamps]
        timestamps.sort(key=lambda tup: tup[0])

        # retrieve right age templates
        etf_path, pfsx_path = choose_template()

        # create
        print("making the eaf file")
        create_eaf(etf_path,record[0]+eaf_type, output_dir, timestamps)
        shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(record[0]+'_'+eaf_type)))
        selected=create_output_csv(record[0], timestamps, os.path.join(output_dir,"{}.csv".format(record[0]+'_'+eaf_type)))

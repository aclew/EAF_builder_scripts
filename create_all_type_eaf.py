import sys, os, shutil
import pandas as pd
import random
import csv
import itertools
import sox
import numpy as np
import pympi
from utils import choose_onsets_periodic, choose_onsets_random,create_eaf,create_output_csv,choose_template, get_time_adjustements


"""
Creates a generic eaf, proper both to random and periodic method
"""
def create_all_type_eaf(folder,output_dir,onset_function,eaf_type,t,contx_onset,contx_offset,template,*args):
    """
    Create eaf files from wav files, in random or periodic onset choice
    Args: 
        folder:a folder which contains wav files to proccess
        onset_function: chosen onset_function for random, periodic or HV eaf files
        eaf_type: random / periodic
        contx_onset:Context onset and code onset difference
        contx_offset: Context offset and code offset difference
        *args: for being able to call different arguments for periodic and random methods
    Returns: 
        output_dir:a folder which contains eafs for each wav file of input filder
    """


    os.makedirs(output_dir, exist_ok=True)
    record_list = []
 
    for dirpath, dirnames, wavfiles in os.walk(folder): #getting into folder for proccessing files
        files= [f for f in wavfiles if f.endswith(".wav")] #exclude Ds.store
        its=[f for f in wavfiles if f.endswith(".its")]
        for f in files:
            duration=sox.file_info.duration(dirpath+'/'+f) #get duration by path to file
            record_list.append([f.split('.')[0],dirpath+'/'+f,duration]) #list[file_id, file, file_duration]
  
    for record in record_list:
        # choose regions (5 by default)
        timestamps = onset_function(int(record[2]),args,t) #onset fix, should be generic for every type of eaf
        timestamps.sort(key=lambda tup: tup[0])
        print("timestamps: ",len(timestamps))
        # retrieve right age templates
        etf_path, pfsx_path = choose_template(template)

        # create
        print("making the eaf file")
        create_eaf(etf_path,record[0]+'_'+eaf_type+'_'+template, output_dir, timestamps,eaf_type,contx_onset,contx_offset,template,None)
        shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(record[0]+'_'+eaf_type+'_'+template)))
        create_output_csv(record[0], timestamps, os.path.join(output_dir,"{}.csv".format(record[0]+'_'+eaf_type+'_'+template)),contx_onset,contx_offset,None)


def create_all_type_eaf_multiple(folder,output_dir,onset_function,eaf_type,t,contx_onset,contx_offset,template,n_its,its_types,overlap,*args):
    """
    Create eaf files from wav files, with a supplemantary csv information (its, rttm etc.) in addition to random / periodic methods
    Args: 
        folder:a folder which contains wav files to proccess
        onset_function: chosen onset_function for random, periodic or HV eaf files
        eaf_type: random / periodic
        contx_onset:Context onset and code onset difference
        contx_offset: Context offset and code offset difference
        template : native /non-native
        n_its: number of its segments to process
        its_types: list of its information types to process (CVC, CTC, AWC)
        overlap: if overllaping time segments are permitted between periodic/random methods and its information
        *args: for being able to call different arguments for periodic and random methods
    Returns: 
        output_dir:a folder which contains eafs for each wav file of input filder
    """


    os.makedirs(output_dir, exist_ok=True)
    record_list = []
 
    for dirpath, dirnames, wavfiles in os.walk(folder): #getting into folder for proccessing files
        files= [f for f in wavfiles if f.endswith(".wav")] #exclude Ds.store
        its=[f for f in wavfiles if f.endswith(".its")]
        for f in files:
            duration=sox.file_info.duration(dirpath+'/'+f) #get duration by path to file
            if f.split('.')[0]+".its" in its:
                record_list.append([f.split('.')[0],dirpath+'/'+f,duration,dirpath+'/'+f.split('.')[0]+'.its']) #list[file_id, file, file_duration,its file attached]
            else:
                record_list.append([f.split('.')[0],dirpath+'/'+f,duration])

  
    for record in record_list:
        print(record)
        timestamps_wav = onset_function(int(record[2]),args,t) #onset fix, should be generic for every type of eaf
        timestamps_wav.sort(key=lambda tup: tup[0])
        if len(record)==4: #if there is an its file to
            timestamps_its=get_time_adjustements(record[3],its_types) #dictionnary for all its types demanded

    
            list_removed=[]
            dict_removed={}
            if overlap.lower() == 'n': #if utilisator doesn't want to have overlap time segments between its information and periodic/random methods
                for start, stop in timestamps_wav:
                    for k, v in timestamps_its.items():
                        list_removed=[]
                        for high,low in v:
                            if (low < start < high) or (low < stop < high): #delate overlapping time lapses
                                list_removed.append((high,low))
                                v.remove((high,low))
                        dict_removed[k]=list_removed
        
                if len(dict_removed.values()) !=0: #if there are delated segements because of overlapping restraction
                    print("WARNING! Removed segments because of overlapping restraction:")
                    print(dict_removed)

            #take n first time segments

            for k,v in timestamps_its.items():
                if int(n_its)>len(v): #if demanded number of time segments are superiour of all conserved time segments:
                    print("Given number of chunks is bigger than the lenght of all chunks. So it's modified to length of all chunks")
                    n_its=len(v)
                timestamps_its[k]=v[:int(n_its)]
            etf_path, pfsx_path = choose_template(template)

            print("making the "+eaf_type+" eaf file and csv")
            create_eaf(etf_path,record[0]+eaf_type+'_'+'its_'+template, output_dir, timestamps_wav,eaf_type,contx_onset,contx_offset,template,timestamps_its)
            shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(record[0]+eaf_type+'_'+'its_'+template)))
            create_output_csv(record[0], timestamps_wav, os.path.join(output_dir,"{}.csv".format(record[0]+'_'+eaf_type+'_its_'+template)),contx_onset,contx_offset)
            for k,v in timestamps_its.items():
                print("making the "+k+" csv file")
                #create csv for all its types
                create_output_csv(record[0], v, os.path.join(output_dir,"{}.csv".format(record[0]+'_'+eaf_type+'_'+template+'_its_'+k)),contx_onset,contx_offset)
        else:
            print("Could not find the .its file for this record. Only random/periodic option to be generated.")
            create_all_type_eaf(folder,output_dir,onset_function,eaf_type,t,contx_onset,contx_offset,template,*args)

import sys, os, shutil
import pandas as pd
import random
import csv
import itertools
import sox
import numpy as np
import pympi
from rpy2 import robjects as r
from datetime import datetime, date, time

def choose_template(template):
    """
    Update: Choose between three template.Basic, native and non-native.
    """
    if template == 'basic':
        return 'etf_templates/ACLEW-basic-template_all-tiers.etf', 'etf_templates/ACLEW-basic-template_all-tiers.pfsx'
    if template == 'native':
        return 'etf_templates/ACLEW-LAAC-native.etf','etf_templates/ACLEW-LAAC-native.pfsx'
    if template == 'non-native':
        return 'etf_templates/ACLEW-LAAC-non-native.etf','etf_templates/ACLEW-LAAC-non-native.pfsx'

def choose_onsets_random(l,n, t, start=10, end=0):
    """
    Function whic sets onset-offset couples in a random way
    Args:
    	int l: length of recording in secondes
    	int n: number of random segments to choose
    	int t: length of the chosen segments for annotation
    	int start: the delay value from the beginnig of the sound file
    	int end: the delay value before the ending of the sound file
    Returns:
    	A list of tuples which contains onset-offset couples in random intervals
    """

    print("choosing random onsets")
    l=int(l/60) #transform seconds to minutes
    minute_tuple_raw_list=[] #tuple of integers (begin_min,end_min) before skip condition applied
    minute_range = list(range(start, min(l - int(t[0]), l-end))) 
    #for some raison t,n and skip 
    #values recovered from argparse have a tuple form like (t,) so we take int(t[0])
    random_minute_range=random.sample(list(minute_range),int(n[0])) #remplaced of shuffle with sample
    minute_tuple_list=[(x, x + int(t[0])) for x in random_minute_range]
    for start, stop in minute_tuple_list:
        for low, high in minute_tuple_raw_list:
            if (low < start < high) or (low < stop < high): #delate overlapping time lapses
                break
        else:
            minute_tuple_raw_list.append((start, stop))
    random_milisec_range=[(x*60000 , y*60000) for x, y in minute_tuple_raw_list]#retranformation to miliseconds for eaf
    return random_milisec_range

def choose_onsets_periodic(l,skip, t, start=34, end=0):
    """Function which sets onset-offset couples with a periodic interstimulus interval (skip)
    Args:
    	int l: length of recording in secondes
    	int skip: interstimulus interval, 60 as default
    	int t: length of the chosen segments for annotation
    	int end: the delay value before the ending of the sound file
    Returns:
    	A list of tuples which contains onset-offset couples in periodic intervals
    """

    print("choosing periodic onsets")
    l=int(l/60) #transform seconds to minutes
    minute_range = [x for x in np.arange(start,min(l - int(t[0]), l-end),int(skip[0])+int(t[0]))] #creates skipped list of numbers
    periodic_minute_range=[(i,i+int(t[0])) for i in minute_range]#creates t min apart tuple couples
    periodic_milisec_range=[(x*60000, y*60000) for x, y in periodic_minute_range] #retranformation to miliseconds for eaf
    return periodic_milisec_range

def compile_files(file):
    """
    This function compiles an r function to access RLena package then do the 
    """
    r.r.source("rlena_extract.R") #access to r file
    output = r.r["rlena_extraction"](file) #access to function
    file_start=pd.read_csv("Time_info.csv",delimiter=',',names=['startClockTime'],skiprows=1)

    file1=pd.read_csv("CVC.csv",delimiter=',',names=['Group.1','x'],skiprows=1)

    #calculate the 
    start_time=datetime.strptime(file_start['startClockTime'].iloc[0],"%Y-%m-%d %H:%M:%S")
    CVC_start=datetime.strptime(file1['Group.1'].iloc[0],"%Y-%m-%d %H:%M")

    startsecCVC=(start_time-CVC_start) #in minutes
    return startsecCVC

def get_time_adjustements(file,its_types):
    """
    This function takes a csv file which contains time informartion and volubility sore information. It transforms time information to 5 min chunks with their respective score, then sort n chunks with highest volubility score.
    Returns a dicionnary as a key its information type ans its timestamps.
    Args:
        its_types:list of demanded its information type: CTC, AWC,CVC
        n: number of chunks
    Retuns:
        A dictionnary.

    """
    dict_time_lapses={}
    startdiff=compile_files(file)
    for i in its_types:
        df=pd.read_csv(i+'.csv',delimiter=',',names=['Group.1','x'],skiprows=1)
        list_onsets=[] #reinitialize for new key
        begin=startdiff.seconds
        print('begin:',begin)
        for index, row in df.iterrows():
            list_onsets.append(((begin,begin+300),row['x'])) #create 5 min time stamps and their score associated
            begin+=300
        list_onsets.sort(key=lambda x:x[1],reverse=True) #sort by the score
        milisec_its_range=[((x*1000 , y*1000),z) for (x, y),z in list_onsets]#retranformation to miliseconds for eaf
        dict_time_lapses[i]=milisec_its_range
    return dict_time_lapses #return n chunks demanded

def create_eaf(etf_path, id, output_dir, timestamps_list, eaf_type,contxt_on, contxt_off,template,its_timestamps_dict):
    
    print("ACLEW ID: ", id)
    eaf = pympi.Elan.Eaf(etf_path)
    ling_type = "transcription"
    eaf.add_tier("code_"+eaf_type, ling=ling_type)
    eaf.add_tier("context_"+eaf_type, ling=ling_type)
    eaf.add_tier("code_num_"+eaf_type, ling=ling_type)
    for i, ts in enumerate(timestamps_list):
        print("Creating eaf code segment # ", i+1)
        print("enumerate makes: ", i, ts)
        whole_region_onset = ts[0]
        whole_region_offset = ts[1]
        #print whole_region_offset, whole_region_onset
        context_onset = int(float(whole_region_onset) - float(contxt_on)*60000)
        #for float / integer unmatch float()
        context_offset = int(float(whole_region_offset) + float(contxt_off)*60000)
        if context_onset < 0:
            context_onset = 0.0
        codeNumVal = eaf_type + str(i+1)
        eaf.add_annotation("code_"+eaf_type, whole_region_onset, whole_region_offset)
        eaf.add_annotation("code_num_"+eaf_type, whole_region_onset, whole_region_offset, value=codeNumVal)
        eaf.add_annotation("context_"+eaf_type, context_onset, context_offset)
    if its_timestamps_dict!=None: #if there is its files to add
        for k,v in its_timestamps_dict.items(): #its types timestamps dictionnary
            eaf.add_tier("code_"+k, ling=ling_type)
            eaf.add_tier("context_"+k, ling=ling_type)
            eaf.add_tier("code_num_its"+k, ling=ling_type)
            eaf.add_tier("notes", ling=ling_type)
            eaf.add_tier("remember-me", ling=ling_type)
            for i,((on,off),score) in enumerate(v):
                print("Creating eaf code segment # ", i+1)
                context_beg = int(float(on) - float(contxt_on)*60000)
                context_end = int(float(off) + float(contxt_off)*60000)
                if context_beg<0:
                    context_beg==0.0
                codeNumVal = k + str(i+1)
                eaf.add_annotation("code_"+k, int(on), int(off))
                eaf.add_annotation("code_num_its"+k, int(on), int(off), value=codeNumVal)
                eaf.add_annotation("context_"+k, context_beg, context_end)
    eaf.to_file(os.path.join(output_dir, "{}.eaf".format(id)))
    for i in eaf.get_tier_names():
        print(i,":",eaf.get_annotation_data_for_tier(i))
    return eaf

def create_output_csv(id, timestamps_list, file_name,context_onset,context_offset):
    '''Creates a csv output of created eafs
    '''
    selected = pd.DataFrame(columns = ['id', 'clip_num', 'onset', 'offset','context_onset','context_offset'], dtype=int)
    for i, ts in enumerate(timestamps_list):
        selected = selected.append({'id': id,
                                    'clip_num': i+1,
                                    'onset': ts[0],
                                    'offset': ts[1],
                                    'context_onset': int(float(ts[0])-float(context_onset)),
                                    'context_offset': int(float(ts[1])+float(context_offset))},
                                    ignore_index=True)
    selected[['id', 'clip_num', 'onset', 'offset','context_onset','context_offset']] = selected[['id', 'clip_num', 'onset', 'offset','context_onset','context_offset']]
    selected.to_csv(file_name,index=False)

def create_output_csv_its(id, timestamps_list, file_name,context_onset,context_offset):
    '''Creates a csv output of created eafs for its file with score 
    '''
    selected = pd.DataFrame(columns = ['id', 'clip_num', 'onset', 'offset','context_onset','context_offset'], dtype=int)
    for i, ((ts1,ts2),score) in enumerate(timestamps_list):
        selected = selected.append({'id': id,
                                    'clip_num': i+1,
                                    'onset': ts1,
                                    'offset': ts2,
                                    'context_onset': int(float(ts1)-float(context_onset)),
                                    'context_offset': int(float(ts2)+float(context_offset)),
                                    'score':score},
                                    ignore_index=True)
    selected[['id', 'clip_num', 'onset', 'offset','context_onset','context_offset','score']] = selected[['id', 'clip_num', 'onset', 'offset','context_onset','context_offset','score']]
    selected.to_csv(file_name,index=False)


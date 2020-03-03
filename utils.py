import sys, os, shutil
import pandas as pd
import random
import csv
import itertools
import sox
import numpy as np
import pympi

def choose_template():
    """
    Update: We have only one templates to use; all tiers
    """
    return 'etf_templates/ACLEW-basic-template_all-tiers.etf', 'etf_templates/ACLEW-basic-template_all-tiers.pfsx'

def choose_onsets_random(l,skip,n=15, t=2, start=10, end=10):
    """
    Function whic sets onset times in a random way
    
    int l: length of recording in minutes
    int n: number of random segments to choose
    int t: length of region of interest (including context)
    int start: minute at which
    """
    print("choosing random onsets")
    minute_tuple_raw_list=[] #tuple of integers (begin_min,end_min) before skip condition applied
    minute_range = list(range(start, min(l - t, l-end)))
    random_minute_range=random.sample(list(minute_range),n) #remplaced of shuffle with sample
    minute_tuple_list=[(x, x + t) for x in random_minute_range]
    for start, stop in minute_tuple_list:
        for low, high in minute_tuple_raw_list:
            if (low < start < high) or (low < stop < high): #delate overlapping time lapses
                break
        else:
            minute_tuple_raw_list.append((start, stop))
    print(minute_tuple_raw_list)
    return minute_tuple_raw_list

def choose_onsets_periodic(l,skip, t=2, start=10, end=10):
    """Function which sets onsets time in a periodic skip version 
    skip: int """
    print("choosing periodic onsets")
    minute_range = [x for x in np.arange(start,min(l - t, l-end),skip+t)] #creates skipped list of numbers
    periodic_minute_range=[(i,i+t) for i in minute_range]#creates t min apart tuple couples
    
    return periodic_minute_range

def create_eaf(etf_path, id, output_dir, timestamps_list, context_before = 1200, context_after = 6000):
    
    print("ACLEW ID: ", id)
    eafob = pympi.Elan.Eaf(etf_path)
    eaf = pympi.Elan.Eaf(etf_path)
    ling_type = "transcription"
    eaf.add_tier("code", ling=ling_type)
    eaf.add_tier("context", ling=ling_type)
    eaf.add_tier("code_num", ling=ling_type)
    eaf.add_tier("on_off", ling=ling_type)
    for i, ts in enumerate(timestamps_list):
        print(timestamps_list)
        print("Creating eaf code segment # ", i+1)
        print("enumerate makes: ", i, ts)
        whole_region_onset = ts[0]
        whole_region_offset = ts[1]
        #print whole_region_offset, whole_region_onset
        roi_onset = whole_region_onset + context_before
        roi_offset = whole_region_offset - context_after
        if roi_onset < 0:
            roi_onset = 0.0
        print("context range: ", whole_region_onset, whole_region_offset)
        print("code range: ", roi_onset, roi_offset)
        print("on_off: ", "{}_{}".format(roi_onset, roi_offset))
        codeNumVal = "HV-" + str(i+1)
        print("code_num", codeNumVal)
        eaf.add_annotation("code", roi_onset, roi_offset)
        eaf.add_annotation("code_num", roi_onset, roi_offset, value=codeNumVal)
        eaf.add_annotation("on_off", roi_onset, roi_offset, value="{}_{}".format(roi_onset, roi_offset))
        eaf.add_annotation("context", whole_region_onset, whole_region_offset)
    eaf.to_file(os.path.join(os.path.dirname(output_dir), "{}.eaf".format(id)))
    return eaf

def create_output_csv(id, timestamps_list, context_before = 1200, context_after = 60000):
    '''Creates a csv output of created templates
    '''
    print("Making output csv...")
    selected = pd.DataFrame(columns = ['id', 'clip_num', 'onset', 'offset'], dtype=int)
    for i, ts in enumerate(timestamps_list):
        selected = selected.append({'id': id,
                                    'clip_num': i+1,
                                    'onset': ts[0]+context_before,
                                    'offset': ts[1]-context_after},
                                    ignore_index=True)
    # selected[['id', 'clip_num', 'onset', 'offset']] = selected[['id', 'clip_num', 'onset', 'offset']].astype(int)
    return selected


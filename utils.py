#import pandas as pd
import constants
import pympi
import random
import os, shutil


def choose_template(age):

    print("Choosing template...")
    
    if 0 <= age <= 7:
        print "age range: 0-7"
        return 'etf_templates/ACLEW-basic-template_00-07mo.etf', 'etf_templates/ACLEW-basic-template_00-07mo.pfsx'
    elif 8 <= age <= 18:
        print "age range: 8-18"
        return 'etf_templates/ACLEW-basic-template_08-18mo.etf', 'etf_templates/ACLEW-basic-template_08-18mo.pfsx'
    elif 19 <= age <= 36:
        print "age range: 19-36"
        return 'etf_templates/ACLEW-basic-template_19-36mo.etf', 'etf_templates/ACLEW-basic-template_19-36mo.pfsx'

def overlap(x, y, t):
    if y < x < y+t:
        return True
    elif y-t < x < y:
        return True
    return False

def choose_onsets(l, n=5, t=5, start=30, end=10):
    """
    Depreciated
    
    int l: length of recording in minutes
    int n: number of random segments to choose
    int t: length of region of interest (including context)
    int start: minute at which
    """
    print("choosing onsets")
    minute_range = range(start, min(l - t, l-end))
    random.shuffle(minute_range)
    selected = []
    for x in minute_range:
        if len(selected) >= n:
            break
        if not any(overlap(x, y, t) for y in selected):
            selected.append(x)
    return [(x, x + t) for x in selected]


def create_eaf(etf_path, id, output_dir, timestamps_list, context_before = 120000, context_after = 60000):
    eaf = pympi.Eaf(etf_path)
    ling_type = "transcription"
    eaf.add_tier("code", ling=ling_type)
    eaf.add_tier("context", ling=ling_type)
    eaf.add_tier("code_num", ling=ling_type)
    eaf.add_tier("on_off", ling=ling_type)
    for i, ts in enumerate(timestamps_list):
        print "Creating eaf code segment # ", i+1
        whole_region_onset = ts[0]
        whole_region_offset = ts[1]
        #print whole_region_offset, whole_region_onset
        # TODO: add sanity checks for timestamps -> make it so you can't go before a file start time, nor go after a file endtime
        roi_onset = float(whole_region_onset) - context_before
        roi_offset = float(whole_region_offset) + context_after
        if roi_onset < 0:
            roi_onset = 0.0
        print roi_onset, roi_offset
        eaf.add_annotation("code", roi_onset, roi_offset)
        eaf.add_annotation("code_num", roi_onset, roi_offset, value=str(i+1))
        eaf.add_annotation("on_off", roi_onset, roi_offset, value="{}_{}".format(roi_onset, roi_offset))
        eaf.add_annotation("context", whole_region_onset, whole_region_offset)
    eaf.to_file(os.path.join(output_dir, "{}.eaf".format(id)))
    return eaf

def create_output_csv(id, timestamps_list, context_before = 120000, context_after = 60000):
    '''
    Depreciated, since input csv has code block times :)
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

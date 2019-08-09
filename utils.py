#import pandas as pd
import constants
import pympi
import random
import os, shutil

import sys
import glob
import xml.etree.ElementTree
from collections import defaultdict


def choose_template(age):

    print("Choosing template...")
    
    if 0 <= age <= 7:
        print "age range: 0-7"
        return 'etf_templates/ACLEW-basic-template_00-07mo.etf', 'etf_templates/ACLEW-basic-template_00-07mo.pfsx'
    elif 8 <= age:
        print "age range: 8+"
        return 'etf_templates/ACLEW-basic-template_08-18mo.etf', 'etf_templates/ACLEW-basic-template_08-18mo.pfsx'

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
    print "ACLEW ID: ", id
    eafob = pympi.Elan.Eaf(etf_path)
    eaf = pympi.Elan.Eaf(etf_path)
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
        roi_onset = whole_region_onset + context_before
        roi_offset = whole_region_offset - context_after
        if roi_onset < 0:
            roi_onset = 0.0
        print "context range: ", whole_region_onset, whole_region_offset
        print "code range: ", roi_onset, roi_offset
        print "on_off: ", "{}_{}".format(roi_onset, roi_offset)
        codeNumVal = "HV-" + str(i+1)
        eaf.add_annotation("code", roi_onset, roi_offset)
        eaf.add_annotation("code_num", roi_onset, roi_offset, value=codeNumVal)
        eaf.add_annotation("on_off", roi_onset, roi_offset, value="{}_{}".format(roi_onset, roi_offset))
        eaf.add_annotation("context", whole_region_onset, whole_region_offset)
        
    #Create Header and other xml info :)
    #e = xml.etree.ElementTree.parse(etf_path).getroot()

    #cvs = eafob.get_controlled_vocabulary_names()
    #for atype in e.findall('CONTROLLED_VOCABULARY'):
     #   CV_ID= ""
      #  EXT_REF= ""
       # for name, value in atype.attrib.items():
        #    if name=="CV_ID":
         #       CV_ID = value
          #  if name=="EXT_REF":
           #     EXT_REF = value
        #eaf.add_controlled_vocabulary(CV_ID,ext_ref=EXT_REF)

    #ext_refs = eafob.get_external_ref_names()
    #for key in ext_refs:
     #   tmp = (eafob.get_external_ref(key))
      #  eaf.add_external_ref(key,tmp[0],tmp[1])



    #what about context
    #for key,val in eaf.get_properties():
     #   eaf.add_property(key,val)
    #pympi.Elan.to_eaf(os.path.join(sys.argv[2],os.path.basename(etf_path)),eaf)
        
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

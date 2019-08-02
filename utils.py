import pandas as pd
import constants
import pympi
import random
import os, shutil


def choose_template(age):
    if 0 <= age <= 7:
            return constants.basic_00_07, constants.basic_00_07_pfsx
    elif 8 <= age <= 18:
            return constants.basic_08_18, constants.basic_08_18_pfsx
    elif 19 <= age <= 36:
            return constants.basic_19_36, constants.basic_19_36_pfsx

def overlap(x, y, t):
    if y < x < y+t:
        return True
    elif y-t < x < y:
        return True
    return False

def choose_onsets(l, n=5, t=5, start=30, end=10):
    """
    int l: length of recording in minutes
    int n: number of random segments to choose
    int t: length of region of interest (including context)
    int start: minute at which
    """
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
        whole_region_onset = ts[0]
        whole_region_offset = ts[1]
        roi_onset = whole_region_onset + context_before
        roi_offset = whole_region_offset - context_after
        eaf.add_annotation("code", roi_onset, roi_offset)
        eaf.add_annotation("code_num", roi_onset, roi_offset, value=str(i+1))
        eaf.add_annotation("on_off", roi_onset, roi_offset, value="{}_{}".format(roi_onset, roi_offset))
        eaf.add_annotation("context", whole_region_onset, whole_region_offset)
    eaf.to_file(os.path.join(output_dir, "{}.eaf".format(id)))
    return eaf

def create_output_csv(id, timestamps_list, context_before = 120000, context_after = 60000):
    selected = pd.DataFrame(columns = ['id', 'clip_num', 'onset', 'offset'], dtype=int)
    for i, ts in enumerate(timestamps_list):
        selected = selected.append({'id': id,
                                    'clip_num': i+1,
                                    'onset': ts[0]+context_before,
                                    'offset': ts[1]-context_after},
                                    ignore_index=True)
    # selected[['id', 'clip_num', 'onset', 'offset']] = selected[['id', 'clip_num', 'onset', 'offset']].astype(int)
    return selected

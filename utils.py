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

def choose_onsets_random(l,n=15, t=2, start=10, end=10):
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
            
    return minute_tuple_raw_list

def choose_onsets_periodic(l,skip, t=2, start=10, end=10):
    """Function which sets onsets time in a periodic skip version 
    skip: int """
    print("choosing periodic onsets")
    minute_range = [x for x in np.arange(start,min(l - t, l-end),skip+t)] #creates skipped list of numbers
    periodic_minute_range=[(i,i+t) for i in minute_range]#creates t min apart tuple couples
    
    return periodic_minute_range


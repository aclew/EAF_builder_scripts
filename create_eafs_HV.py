# Edited by Sarah MacEwan
# Aug 2, 2019

import sys, os, shutil
#import pandas as pd
import constants, utils
import random

import csv

def readCSV():

    # TODO: add in checks for exceptions (which operate on their own # of clips, rather than on 15 clips/recording)

    output_dir = sys.argv[2]
    
    record_list = set([])
    clipCount = 0
    rNum = 0
    clipTimes = []
    clipAges = []
    with open(sys.argv[1]) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            #print rNum
            if rNum == 0:
                rNum = rNum+1
                continue
            else:
                record_list.add(row[0])
                #print row
                #print record_list
                clipName = row[1].split('_')
                #print "clip name is: ", clipName
                tStart = int(float(clipName[3])*1000)
                tEnd = int(float(clipName[4])*1000)
                clipTimes.append([tStart, tEnd])
                age = row[2]
                clipAges.append(age)
                #print "clip times: ", clipTimes
                #print clipAges
            #clipCount +=1
            #if clipCount >= 14:
            #   clipCount = 0
            rNum = rNum+1
    startRange = 0
    for recording in record_list:
        # TODO: add in checks for exceptions (which operate on their own # of clips, rather than on 15 clips/recording)
        babyAge = int(clipAges[startRange])
        print "baby age is: ", babyAge
        etf_path, pfsx_path = utils.choose_template(babyAge)
        timestamps = clipTimes[startRange:startRange+15]
        print "timestamps: ", timestamps
        utils.create_eaf(etf_path, recording, output_dir, timestamps)
        shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(recording)))
        startRange = startRange + 15

def main():

    '''
    Depreciated code
    '''

    print("iterating through input csv...")

    clips_list = pd.read_csv(sys.argv[1])
    output_dir = sys.argv[2]

    selected = pd.DataFrame(columns = ['id', 'clip_num', 'onset', 'offset'], dtype=int)
    
    record_list = set([])
 
    for clip in clips_list:
        record_list.add(clip[0])
        print "record list is currently...: ", record_list
        

#    for i, record in record_list.iterrows():
#        print(record.index)
#        # choose regions (5 by default)
#       timestamps = utils.choose_onsets(int(record.length_of_recording), n=15)
 #       timestamps = [(x * 60000, y * 60000) for x, y in timestamps]
 #       timestamps.sort(key=lambda tup: tup[0])
 #       print(timestamps)
#
#        # retrieve right age templates
#        etf_path, pfsx_path = utils.choose_template(record.age)
#
#        # create
#        print("making the eaf file")
#        utils.create_eaf(etf_path, record.id, output_dir, timestamps)
#        shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(record.id)))
#
#        selected = pd.concat([selected, utils.create_output_csv(record.id, timestamps)])
#
#
#
 #   selected[['clip_num', 'onset', 'offset']] = selected[['clip_num', 'onset', 'offset']].astype(int)
 #   selected.to_csv(os.path.join(output_dir,'selected_regions.csv'), index=False)
#
#
if __name__=="__main__":
    readCSV()

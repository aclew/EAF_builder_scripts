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
    
    record_list = []
    clipCount = 0
    rNum = 0
    clipTimes = []
    clipAges = []
   # exceptionList = set([])
    #exceptionTimes[]
    #exceptionAges[]
    with open(sys.argv[1]) as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            #print rNum
            if rNum == 0:
                rNum = rNum+1
                continue
            else:
                #if row[-2] == "standard":
                 #   print row[-2]
                record = row[0]
                if not record in record_list:
                    record_list.append(record)
                    print "added ", record, "to record list!"
                #print row
                print record_list
                clipName = row[1].split('_')
                #print "clip name is: ", clipName
                tStart = int(float(clipName[3])*1000)
                tEnd = int(float(clipName[4])*1000)
                clipTimes.append([row[0], tStart, tEnd])
                age = row[2]
                clipAges.append(age)
 #               else:
  #                  print row[-2]
   #                 exceptionlist.add(row[0])
    #                clipName = row[1].split('_')
     #               print "clip name is: ", clipName
      #              tStart = int(float(clipName[3])*1000)
       #             tEnd = int(float(clipName[4])*1000)
        #            exceptionTimes.append([tStart, tEnd])
         #           age = row[2]
          #          exceptionAges.append(age)
                #print "clip times: ", clipTimes
                #print clipAges
            #clipCount +=1
            #if clipCount >= 14:
            #   clipCount = 0
            rNum = rNum+1
    startRange = 0
    listLen = len(clipTimes)
    print "clip Times: "
    print clipTimes
    for recNum in range(len(record_list)):
        print "starting new recording"
        recording = record_list[recNum]
        babyAge = int(clipAges[startRange])
        print "baby age is: ", babyAge
        etf_path, pfsx_path = utils.choose_template(babyAge)
        timestamps = []
        itercount = startRange
        num_clips = 0
        timeData = clipTimes[startRange]
        print "initial time data = ", timeData
        rec = timeData[0]
        print "start range: ", startRange
        print "rec = ", rec, "recording = ", recording
        while rec == recording and itercount < listLen-1:
            print "start range: ", startRange, "itercount: ", itercount
            # TODO: add in checks for exceptions (which operate on their own # of clips, rather than on 15 clips/recording)
            timestamps.append(clipTimes[itercount])
            itercount += 1
            timeData = clipTimes[itercount]
            rec = timeData[0]
            print "time data = ", timeData, " and rec is: ", rec
            num_clips += 1
            print "num clips = ", num_clips
        print "timestamps: ", timestamps
        if len(timestamps) >1:
            utils.create_eaf(etf_path, recording, output_dir, timestamps)
            shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(recording)))
        else:
            print "error, timestamps were empty D:"
        startRange = startRange + num_clips
    #for reco in exceptionList:
     #   babyAge = int(clipAges[startRange])
      #  print "baby age is: ", babyAge
       # etf_path, pfsx_path = utils.choose_template(babyAge)
        #timestamps = clipTimes[startRange:startRange+15]
        #print "timestamps: ", timestamps
   #     utils.create_eaf(etf_path, recording, output_dir, timestamps)
   #     shutil.copy(pfsx_path, os.path.join(output_dir, "{}.pfsx".format(recording)))
   #     startRange = startRange + 15

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

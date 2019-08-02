
from __future__ import print_function
import sys
import glob  # Import glob to easily loop over files
import pympi  # Import for EAF file read
import warnings
from collections import defaultdict
#from pathlib import Path
import os
import random
import xml.etree.ElementTree


# removing warnings
warnings.filterwarnings("ignore")

# if we fix tier names
# tier_names = ['FA1', 'FA2','CHI']#code_num,on_off, context, code
ignore_tier_names=['code_num','on_off', 'context','code','notes','UC*']

#if the output file exists, delete it!
if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

def add_child_tiers(new_eaf,tier_name,eafob):
    child_tiers = eafob.get_child_tiers_for(tier_name)
    # if child_tiers is not None:
    for child_tier in child_tiers:
        print(child_tier.split("@")[0])
        new_eaf.add_tier(child_tier,ling =child_tier.split("@")[0].upper(),parent=tier_name)
        add_child_tiers(new_eaf,child_tier,eafob)

file_dist_list = dict()
# loop over all the EAF files in the output folder
for file_path in glob.glob('{}/*.eaf'.format(sys.argv[1])):
    code_blocks_mutable = list()
    code_blocks_selected = list()
    file_name = os.path.basename(file_path)
    print('File Name: {}'.format(file_name))
    # Initialize the elan file
    eafob = pympi.Elan.Eaf(file_path)
    code_blocks = eafob.get_annotation_data_for_tier('code')

    for i in range(0, len(code_blocks)):
        if 'random-' in code_blocks[i][2]:
            code_blocks_mutable.append((code_blocks[i][0],code_blocks[i][1],code_blocks[i][2],0,0))#first, second minute
    # print(code_blocks_mutable)
    res = (item for item in code_blocks if item[0]==10980000)# print(blocks)
    tier_names = eafob.get_tier_names()
    for tier_name in tier_names:
        if tier_name not in ignore_tier_names and "@" not in tier_name :
            annotations = eafob.get_annotation_data_for_tier(tier_name)
            for annotation in annotations:
                if len(annotation[2]) >2:#if empty
                    for i in range(0,len(code_blocks_mutable)):
                        t = list(code_blocks_mutable[i])
                        if annotation[0]>=t[0] and annotation[1]<=t[1]:#check if they are in between
                            if annotation[0]<t[0]+1*60*1000:#inside 1st minute mark
                                t[3]+=  annotation[1]-annotation[0]#add timestamps
                            else:
                                t[4] += annotation[1]-annotation[0]


                        code_blocks_mutable[i] = tuple(t)

    code_blocks_mutable.sort(key=lambda tup: tup[4]-tup[3],reverse=True)
    # print(code_blocks_mutable)
    file_dist_list[file_name] = 0
    for code_block in code_blocks_mutable:
        file_dist_list[file_name]+=code_block[4]-code_block[3]

    # print(os.path.basename(file_path))
    if os.path.exists(os.path.join(sys.argv[2],"output_"+os.path.basename(file_path))):
        os.remove(os.path.join(sys.argv[2],"output_"+os.path.basename(file_path)))
    # open("output.eaf", "w")
    ###creating new eaf
    new_eaf = pympi.Elan.Eaf(author='John')
    new_eaf.add_tier("notes")
    new_eaf.add_tier("context")
    new_eaf.add_tier("code_num")
    new_eaf.add_tier("code")
    ling_types = eafob.get_linguistic_type_names()
    for ling in ling_types:
        new_eaf.add_linguistic_type(lingtype=ling, param_dict=eafob.get_parameters_for_linguistic_type(ling))

    # new_eaf.add_tier("CHI")

    for code_blocks in code_blocks_mutable:
        if code_blocks[4] >0 or code_blocks[3] >0 :
            code_blocks_selected.append((code_blocks[0],code_blocks[1],code_blocks[2],code_blocks[3],code_blocks[4]))
    # selected_second = 0
    # selected_first=len(code_blocks_selected)-1
    start_time = selected = 0
    if file_dist_list[file_name]< 0:
        selected= (random.randint(0,int(.5*len(code_blocks_selected)-1)))
        start_time = code_blocks_selected[selected][0]+60000
    else:
        selected = random.randint((int(.5 * len(code_blocks_selected)-1))+1,len(code_blocks_selected)-1)
        start_time = code_blocks_selected[selected][0]

    # selected_first = random.randint((int(.5 * len(code_blocks_selected)-1))+1,len(code_blocks_selected)-1)
    # print(code_blocks_selected[selected_second])
    # print(code_blocks_selected[selected_first])

    #tiers that you want in the output
    tier_names = ['FA1', 'CHI'] #eafob.get_tier_names()
    for tier_name in tier_names:
        # if tier_name in tier_names or "@" not in tier_name:
        new_eaf.add_tier(tier_name)
        add_child_tiers(new_eaf,tier_name,eafob)

    # start_times_considering = [code_blocks_selected[selected][0]+60000, code_blocks_selected[selected][0]]
    # for start_time in start_times_considering:

    #second minute add
    new_eaf.add_annotation("code", start_time, start_time+60000) #adding 1 minute from the start
    new_eaf.add_annotation("code_num", start_time,start_time+60000, value= '1')
    new_eaf.add_annotation("context", start_time-60000, start_time+2*60000)
    e = xml.etree.ElementTree.parse(file_path).getroot()

    cvs = eafob.get_controlled_vocabulary_names()
    for atype in e.findall('CONTROLLED_VOCABULARY'):
        CV_ID= ""
        EXT_REF= ""
        for name, value in atype.attrib.items():
            if name=="CV_ID":
                CV_ID = value
            if name=="EXT_REF":
                EXT_REF = value
        new_eaf.add_controlled_vocabulary(CV_ID,ext_ref=EXT_REF)

    ext_refs = eafob.get_external_ref_names()
    for key in ext_refs:
        tmp = (eafob.get_external_ref(key))
        new_eaf.add_external_ref(key,tmp[0],tmp[1])

    #what about context
    for key,val in eafob.get_properties():
        new_eaf.add_property(key,val)
    pympi.Elan.to_eaf(os.path.join(sys.argv[2],"rely_"+os.path.basename(file_path)),new_eaf)
    # break

file_dist_list = sorted(file_dist_list.items(), key=lambda kv: kv[1])
print(file_dist_list)
    # code_blocks_mutable.sort(key=lambda tup: tup[4], reverse=True)
    # print(code_blocks_mutable)
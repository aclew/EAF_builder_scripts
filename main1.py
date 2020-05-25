from create_all_type_eaf import create_all_type_eaf, create_all_type_eaf_multiple
from utils import choose_onsets_periodic, choose_onsets_random,create_eaf,create_output_csv,choose_template
import argparse
import pandas as pd
import csv
"""
Main code for the activation of script.
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('wav_folder', default=None, help='Folder which contains wav files for Eaf extraction')
    parser.add_argument('output_folder', default=None, help='Folder which will contains newly created eaf templates for wav files')
    parser.add_argument('--eaf_type', default=None, help='Random or Periodic or None')
    parser.add_argument('--t',help='Length of extracted chunks for periodic and random')
    parser.add_argument('--n',help='number of chunks selected for random methods')
    parser.add_argument('--skip',help='Interstimulis interval for periodic method')
    parser.add_argument('--c_on',help='Context onset and actual code onset difference')
    parser.add_argument('--c_off',help='Context offset and actual code offset difference')
    parser.add_argument('--temp',help='Type "basic","native" or "non-native" up to your choice of ACLEW template.')
    parser.add_argument('--its',help='y or n')
    parser.add_argument('--n_its',help='Number of its chunks to be extracted')
    parser.add_argument('--its_types',nargs='+',help='list of demanded its information, should type a list with spaces between args ')
    parser.add_argument('--overlap',help='Type "y" if you allow periodic/random time segments to overlap with its time segements. "n" otherwise')
    

    args= parser.parse_args()
    list_params=[]
    #Treating different EAF options
    if args.eaf_type.lower()=='periodic':
        if args.its.lower()=='y': #if its information demanded
            create_all_type_eaf_multiple(args.wav_folder,args.output_folder,choose_onsets_periodic,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap,args.skip)
            list_params=[args.wav_folder,args.eaf_type,args.t,args.skip,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap]
            write_parameters(list_params,args.output_folder,args.eaf_type,args.its)
        else:
            create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_periodic,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.skip)
            list_params=[args.wav_folder,args.eaf_type,args.t,args.skip,args.c_on,args.c_off,args.temp]
            write_parameters(list_params,args.output_folder,args.eaf_type,args.its)
    if args.eaf_type.lower()=='random':
        if args.its.lower()=='y':#if its information demanded
            create_all_type_eaf_multiple(args.wav_folder,args.output_folder,choose_onsets_random,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap,args.n)
            list_params=[args.wav_folder,args.eaf_type,args.t,args.n,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap]
            write_parameters(list_params,args.output_folder,args.eaf_type,args.its)
        else:
            create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_random,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n)
            list_params=[args.wav_folder,args.eaf_type,args.t,args.n,args.c_on,args.c_off,args.temp]
            write_parameters(list_params,args.output_folder,args.eaf_type,args.its)


    elif args.eaf_type.lower()!='random' and args.eaf_type.lower()!='periodic':
        print("Sorry this type of eaf does not exist please type 'random' or 'periodic'.")

def write_parameters(params,folder,eaf_type,its):
    """
    Create a csv file which save pipeline parameters
    """
    print("Writing pipeline parameters to csv.")
    csv_file="{}.csv".format(folder+'/'+'pipeline_parameters')
    
    if eaf_type.lower() == 'random':
        if its.lower()=='y':
            parameters={'wav_folder':params[0], 'eaf_type':params[1],'t':params[2],'n':params[3],'c_on':params[4],'c_off':params[5],'temp':params[6],'n_its':params[7],'its_types':params[8],'overlap':params[9]}
            
        else:

            parameters={'wav_folder':params[0], 'eaf_type':params[1],'t':params[2],'n':params[3],'c_on':params[4],'c_off':params[5],'temp':params[6]}
            
    if eaf_type.lower() == 'periodic':
        if its.lower()=='y':
            parameters={'wav_folder':params[0], 'eaf_type':params[1],'t':params[2],'skip':params[3],'c_on':params[4],'c_off':params[5],'temp':params[6],'n_its':params[7],'its_types':params[8],'overlap':params[9]}
            
        else:
            parameters={'wav_folder':params[0], 'eaf_type':params[1],'t':params[2],'skip':params[3],'c_on':params[4],'c_off':params[5],'temp':params[6]}
    
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, parameters.keys())
            writer.writeheader()
            writer.writerow(parameters)

    except IOError:
        print("I/O error")

if __name__ == "__main__" :

    main()

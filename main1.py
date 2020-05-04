from create_all_type_eaf import create_all_type_eaf, create_all_type_eaf_multiple
from utils import choose_onsets_periodic, choose_onsets_random,create_eaf,create_output_csv,choose_template
import argparse
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
    #Treating different EAF options
    if args.eaf_type.lower()=='periodic':
        if args.its=='y': #if its information demanded
            create_all_type_eaf_multiple(args.wav_folder,args.output_folder,choose_onsets_periodic,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap,args.skip)
        else:
            create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_periodic,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.skip)
    if args.eaf_type.lower()=='random':
        if args.its.lower()=='y':#if its information demanded
            create_all_type_eaf_multiple(args.wav_folder,args.output_folder,choose_onsets_random,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n_its,args.its_types,args.overlap,args.n)
        else:
            create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_random,args.eaf_type,args.t,args.c_on,args.c_off,args.temp,args.n)


    elif args.eaf_type.lower()!='random' and args.eaf_type.lower()!='periodic':
        print("Sorry this type of eaf does not exist please type 'random' or 'periodic'.")


if __name__ == "__main__" :

    main()

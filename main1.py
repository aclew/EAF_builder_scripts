from create_all_type_eaf import create_all_type_eaf
from utils import choose_onsets_periodic, choose_onsets_random,create_eaf,create_output_csv,choose_template
import argparse
"""
Main code for the activation of script.
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('wav_folder', default=None, help='Folder which contains wav files for Eaf extraction')
    parser.add_argument('output_folder', default=None, help='Folder which will contains newly created eaf templates for wav files')
    parser.add_argument('eaf_type', default=None, help='Random or Periodic')
    parser.add_argument('--t',help='Length of extracted chunks')
    parser.add_argument('--n',help='number of chunks selected for random')
    parser.add_argument('--skip',help='Interstimulis interval for periodic method')


    args= parser.parse_args()
    #Treating different EAF options an exceptions
    if args.eaf_type.lower()=='periodic':
        create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_periodic,args.eaf_type,args.t, args.skip)
    if args.eaf_type.lower()=='random':
        create_all_type_eaf(args.wav_folder,args.output_folder,choose_onsets_random,args.eaf_type,args.t,args.n)
    elif args.eaf_type.lower()!='random' and args.eaf_type.lower()!='periodic':
        print("Sorry this type of eaf does not exist please type 'random' or 'periodic'.")


if __name__ == "__main__" :

    main()

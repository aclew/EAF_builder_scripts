# EAF_BUILDER_SCRIPTS -2nd version

This repo contains the script for creating periodicly or randomly selected ELAN templates.

-Utils file contains onset fix tools for random and periodic onset-offset method, as well as an eaf creator function and csv creation function.

-Create_all_type_eaf contains a generic eaf generator code for periodic and random methods.

## PACKAGE REQUIREMENTS:

* pandas
* pympi
* sox
* numpy
* rpy2

## To use this code

Don't forget to install the required packages mentioned above!

```
$ git clone https://github.com/aclew/EAF_builder_scripts.git
$ git checkout -b second-version
```

## A note on the templates

You currently have three choices:

1) ACLEW-basic-template_all-tiers -- as the name indicates
2) ACLEW-LAAC-native -- a variant on ACLEW, the only change being that VCM is also coded in non-CHI tiers
3) ACLEW-LAAC-non-native -- for use when your annotators don't speak the language in the files; it does not include the xds, lex, mwu tiers

## For launching the code:

	python3 main1.py 'path_to_your_wav_folder' 'path_to_new_eaf_store_file' 'periodic or random(choose one)' --t 'int' --n/--skip 'int' (skip if periodic, n if random) --c_on 'int' --c_off 'int' --temp 'basic or native or non-native' --its 'y/n' (if yes) --n_its  'int' --its_types 'list' --overlap 'y/n'

* --t is the length of choosen chunks in minutes
* --skip is the interstimulis interval for the periodic method in minutes
* --n is the number of chunks to be chosen for the random method
* --c_on is the difference between code onset and context onset in minutes
* --c_off is the difference between code offset and context offset in minutes
* --temp is the choice of templates between basic, native or non-native(only vcm for all tiers including CHI)
* --its is the parameter that defines if you want to process its files
* --n_its number of its information chunks to be chosen
* --its_types list of its types needed (AWC, CVC and CTC)
* --overlap the paralater that defines if its information time segments can overlap with main methods(random or periodic) time segments

### SOME EXAMPLES:

	python3 main1.py ../wavs/ ../eafs/ periodic --t 2 --skip 59 --c_on 2 --c_off 3 --temp non-native --its n
output: a periodic extraction on the non-native template every 59 minutes of 2-minutes-long chunks. The context tiers begin 2 minutes before code tier onset and end 3 minutes after the code tier offset without its file processing.

	python3 main1.py ../wavs/ ../eafs/ random --t 2 --n 20 --c_on 1 --c_off 0,5 --temp native --its n
output: a random extraction on the native template of 20 chunks of 2-minutes-long. The context tiers begin 1 minutes before code tier onset and end half a minute after the code tier offset without its file processing.

	python3 main1.py ../wavs/ ../eafs/ periodic --t 1 --skip 30 --c_on 2 --c_off 2 --temp basic --its y --n_its 15 --its_types AWC CVC --overlap n
output: a periodic extraction on the basic template every 30 minutes of 1-minutes-long chunks.The context tiers begin 2 minutes before code tier onset and end 2 minutes after the code tier offset. AWC and CVC its information types are extracted with 15 chunks. Overlap between periodic time segments and its information(AWC, CVC) time segments isn't permitted.

	python3 main1.py ../wavs/ ../eafs/ random --t 3 --n 15 --c_on 0 --c_off 1 --temp non-native --its y --n_its 10 --its_types CTC --overlap y
output: a random extraction on the non-native template of 15 chunks of 3-minutes-long.The context tiers begin at the same time with the code tier onset and end 1 minutes after the code tier offset. CTC its information type is extracted with 10 chunks. Overlap between periodic time segments and its information(CTC) time segments is permitted.


# EAF_BUILDER_SCRIPTS -2nd version

This repo contains the script for creating periodicly or randomly selected ELAN templates.

-Utils file contains onset fix tools for random and periodic onset-offset method, as well as an eaf creator function and csv creation function.

-Create_all_type_eaf contains a generic eaf generator code for periodic and random methods.

## For launching the code:

	python3 main1.py 'path_to_your_wav_folder' 'path_to_new_eaf_store_file' 'periodic or random(choose one)' --t 'int' --n/--skip 'int' (skip if periodic, n if random) --c_on 'int' --c_off 'int'

* --t is the length of choosen chunks
* --skip is the interstimulis interval for the periodic method
* --n is the number of chunks to be chosen for the random method
* --c_on is the difference between code onset and context onset
* --c_off is the difference between code offset and context offset

### SOME EXAMPLES:

	python3 main1.py ../wavs/ ../eafs/ periodic --t 2 --skip 59 --c_on 2 --c_off 3
output: a periodic extraction every 59 minutes of 2-minutes-long chunks. The context tiers begin 2 minutes before code tier onset and end 3 minutes after the code tier offset.

	python3 main1.py ../wavs/ ../eafs/ random --t 2 --n 20 --c_on 1 --c_off 0,5
output: a random extraction of 20 chunks of 2-minutes-long. The context tiers begin 1 minutes before code tier onset and end half a minute after the code tier offset.

	python3 main1.py ../wavs/ ../eafs/ periodic --t 1 --skip 30 --c_on 2 --c_off 2
output: a periodic extraction every 30 minutes of 1-minutes-long chunks.The context tiers begin 2 minutes before code tier onset and end 2 minutes after the code tier offset.

	python3 main1.py ../wavs/ ../eafs/ random --t 3 --n 15 --c_on 0 --c_off 1
output: a random extraction of 15 chunks of 3-minutes-long.The context tiers begin at the same time with the code tier onset and end 1 minutes after the code tier offset.

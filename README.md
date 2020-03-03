EAF_BUILDER_SCRIPTS -2nd version

This repo contains the script for creating periodicly or randomly selected ELAN templates.

-Utils file contains onset fix tools for random and periodic onset-offset method, as well as an eaf creator function and csv creation function.

-Create_all_type_eaf contains a generic eaf generator code for periodic and random methods.

For launching the code:

	python3 create_all_type_eaf.py 'path_to_your_wav_folder' 'path_to_new_eaf_store_file' 'periodic or random(choose one)' skip_number

* skip_number is 0 for random method and up to yout choice for periodic method.
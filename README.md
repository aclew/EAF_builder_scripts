EAF_BUILDER_SCRIPTS -2nd version

This repo contains the script for creating periodicly or randomly selected ELAN templates.

For cloning te repo to your computer type to the terminal:
	git clone https://github.com/aclew/EAF_builder_scripts/tree/Second-Version

-Utils file contains onset fix tools for random and periodic onset-offset method, as well as an eaf creator function and csv creation function.

-Create_all_type_eaf contains a generic eaf generator code for periodic and random methods.

For launching the code:

	python3 main1.py 'path_to_your_wav_folder' 'path_to_new_eaf_store_file' 'periodic or random(choose one)'

* skip_number is 60min periodic method as default. You can change it by utils.py -->choose_onsets_periodic(...,skip='number you want',...)

* for random method segment number is n=15 as default. You can change it by utils.py -->choose_onsets_random(...,n='number you want',...)
# Scripts

## Random samples

### create_eaf_random_regions.py

Usage

```
python create_eaf_random_regions.py path/to/info_spreadsheet.csv path/to/output_dir
```

where:
- `info_spreadsheet.csv` contains (at least) three columns: `id`, `age` and `length_of_recording` (in minutes); you can get that last piece of information using `soxi -D path/to/recording.wav` -- the result will be displayed in seconds.
- `output_dir/` will contain the .eaf and .pfsx files after running the script, as well as the recap spreadsheet of which regions were chosen for each file processed.


## _Notes_

- `etf_templates/` are the basic ACLEW templates
- `constants.py` builds python objects containing the paths to the different etf templates renamed based on age
- `utils.py` contains the functions necessary to compute the non overlapping random regions
- there are different etf templates for different ages, so the info spreadsheet has to contain an `age` column, a `length_of_recording` column and an `id` column containing the name of the recording

# Event_Code_Search
UK Biobank code and event search tool.

## Installation:
Tested with Python version 3.9

It is recommended that you first create a virtual environment before installing

1. Clone/download this repository to your local computer.
2. In the terminal change the work directory to the repository's local lcoation.

```
cd  /user_path/event_code_search/
```

3. Activate/create your virtual environment
e.g. with conda:
``` 
conda create -n event_code_search python=3.9 

conda activate event_code_search
```

or with virtualenv

 ```
python3.9 -m venv /your_path/event_code_search
 
source /your_path/event_code_search/bin/activate
 ```

3. Pip install the package from its directory

```
pip install -e .
```

## Running:

```
event_code_search --dat_path /path_to_outcome_data.csv --pkl_path /path_to_event_data.pkl --output_path /path_to_output --icd10_codes I10 I11 --all_causes_death
```

All code arguments in the command can either be entered as a space-separated list, or if you have a longer list of codes you can use a text file (one code per row in the file):
```--icd10_codes /path_to_codes/icd10_codes.txt```


```
event_code_search -h 
usage: event_code_search [-h] --dat_path DAT_PATH --pkl_path PKL_PATH --output_path OUTPUT_PATH [--icd10_codes ICD10_CODES [ICD10_CODES ...]]
                         [--icd9_codes ICD9_CODES [ICD9_CODES ...]] [--death_icd10_codes DEATH_ICD10_CODES [DEATH_ICD10_CODES ...]] [--opcs4_codes OPCS4_CODES [OPCS4_CODES ...]]
                         [--all_causes_death]

Process and analyze medical event data from the UK Biobank.

optional arguments:
  -h, --help            show this help message and exit
  --dat_path DAT_PATH   Path to the CSV data file containing the dataset.
  --pkl_path PKL_PATH   Path to the pickle file containing preloaded event data.
  --output_path OUTPUT_PATH
                        Directory path for saving the output files.
  --icd10_codes ICD10_CODES [ICD10_CODES ...]
                        List of ICD10 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.
  --icd9_codes ICD9_CODES [ICD9_CODES ...]
                        List of ICD9 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.
  --death_icd10_codes DEATH_ICD10_CODES [DEATH_ICD10_CODES ...]
                        List of Death-related ICD10 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.
  --opcs4_codes OPCS4_CODES [OPCS4_CODES ...]
                        List of OPCS4 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.
  --all_causes_death    Flag to include all-cause mortality in the search.
  ```
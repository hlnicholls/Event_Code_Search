# Event_Code_Search
UKBB ICD code and event search tool.

```
event_code_search --dat_path /path_to_outcome_data.csv --pkl_path /path_to_event_data.pkl --output_path /path_to_output --icd10_codes I10 I11 --all_causes_death
```


```
event_code_search -h 
usage: event_code_search [-h] --dat_path DAT_PATH --pkl_path PKL_PATH --output_path OUTPUT_PATH [--icd10_codes ICD10_CODES [ICD10_CODES ...]]
                         [--icd9_codes ICD9_CODES [ICD9_CODES ...]] [--death_icd10_codes DEATH_ICD10_CODES [DEATH_ICD10_CODES ...]] [--opcs4_codes OPCS4_CODES [OPCS4_CODES ...]]
                         [--all_causes_death]

Process and analyze medical event data from the UK Biobank.

options:
  -h, --help            show this help message and exit
  --dat_path DAT_PATH   Path to the CSV data file containing the dataset.
  --pkl_path PKL_PATH   Path to the pickle file containing preloaded event data.
  --output_path OUTPUT_PATH
                        Directory path for saving the output files.
  --icd10_codes ICD10_CODES [ICD10_CODES ...]
                        List of ICD10 codes of interest. Space-separated if multiple.
  --icd9_codes ICD9_CODES [ICD9_CODES ...]
                        List of ICD9 codes of interest. Space-separated if multiple.
  --death_icd10_codes DEATH_ICD10_CODES [DEATH_ICD10_CODES ...]
                        List of Death-related ICD10 codes of interest. Space-separated if multiple.
  --opcs4_codes OPCS4_CODES [OPCS4_CODES ...]
                        List of OPCS4 codes of interest. Space-separated if multiple.
  --all_causes_death    Flag to include all-cause mortality in the search.
  ```
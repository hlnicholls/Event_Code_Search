import pandas as pd
from datetime import datetime
from collections import defaultdict

class EventSearcher:
    def __init__(self, event_data, event_organiser):
        self.event_data = event_data
        self.event_organiser = event_organiser

    def search_events(self, icd10_codes=None, icd9_codes=None, death_icd10_codes=None, opcs4_codes=None, all_causes_death=False):
        print("Starting search for events...")
        res_df = defaultdict(pd.DataFrame)
        
        # Helper function to process codes and dates, and find minimum dates
        def process_events(event_dict, codes):
            min_date = defaultdict(list)
            for k, v in event_dict.items():
                for icd, dates in v.items():
                    if any(icd.startswith(code) for code in codes):
                        valid_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates if not pd.isna(date)]
                        if valid_dates:  # Check if there are valid dates
                            min_date[k].append(min(valid_dates))
            return min_date
        
        if icd10_codes and 'icd10' in self.event_data:
            print("Processing ICD-10 codes...")
            icd10_dict = self.event_organiser.organiser('icd10')
            min_date = process_events(icd10_dict, icd10_codes)
            res_df['icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'icd10_dx_date': [min(v) for v in min_date.values()]})
        
        # Repeat similar blocks for icd9, death_icd10, and opcs4 as needed...
        
        if all_causes_death:
            print("Processing all-cause death events...")
            death_dict = self.event_organiser.organiser('death_icd10')
            min_date = defaultdict(list)
            for k, v in death_dict.items():
                for icd, dates in v.items():
                    valid_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates if not pd.isna(date)]
                    if valid_dates:
                        min_date[k].append(min(valid_dates))
            res_df['all_cause_death_icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'all_cause_death_icd10_date': [min(v) for v in min_date.values()]})
        
        print("Combining results from different categories...")
        combined_df = pd.DataFrame()
        for key, df in res_df.items():
            df.set_index('feid', inplace=True)
            combined_df = pd.concat([combined_df, df], axis=1)
        
        print("Event search completed.")
        return combined_df.reset_index()

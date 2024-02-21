import pandas as pd
from datetime import datetime
from collections import defaultdict

class EventSearcher:
    def __init__(self, event_data, event_organiser):
        self.event_data = event_data
        self.event_organiser = event_organiser

    def search_events(self, icd10_codes=None, icd9_codes=None, death_icd10_codes=None, opcs4_codes=None, icd10=False, icd9=False, death_icd10=False, opcs4=False, all_causes_death=False):
        print("Starting search for events...")
        res_df = defaultdict(pd.DataFrame)

        # Helper function to process codes and dates, and find minimum dates
        def process_events(event_dict, codes, code_type):
            print(f"Processing {code_type} codes...")
            min_date = defaultdict(list)
            for k, v in event_dict.items():
                for icd, dates in v.items():
                    if any(icd.startswith(code) for code in codes):
                        valid_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates if not pd.isna(date)]
                        if valid_dates:
                            min_date[k].append(min(valid_dates))
            return min_date

        if icd10:
            icd10_dict = self.event_organiser.organiser('icd10')
            min_date = process_events(icd10_dict, icd10_codes, 'ICD-10')
            res_df['icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'icd10_dx_date': [min(v) for v in min_date.values()]})

        if icd9:
            icd9_dict = self.event_organiser.organiser('icd9')
            min_date = process_events(icd9_dict, icd9_codes, 'ICD-9')
            res_df['icd9'] = pd.DataFrame({'feid': list(min_date.keys()), 'icd9_dx_date': [min(v) for v in min_date.values()]})

        if death_icd10:
            death_icd10_dict = self.event_organiser.organiser('death_icd10')
            min_date = process_events(death_icd10_dict, death_icd10_codes, 'Death ICD-10')
            res_df['death_icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'death_icd10_date': [min(v) for v in min_date.values()]})

        if opcs4:
            opcs4_dict = self.event_organiser.organiser('opcs4')
            min_date = process_events(opcs4_dict, opcs4_codes, 'OPCS-4')
            res_df['opcs4'] = pd.DataFrame({'feid': list(min_date.keys()), 'opcs4_date': [min(v) for v in min_date.values()]})

        if all_causes_death:
            print("Processing all-cause death events...")
            # Assuming all death codes are relevant for all-cause mortality
            death_dict = self.event_organiser.organiser('death_icd10')
            min_date = defaultdict(list)
            for k, v in death_dict.items():
                for icd, dates in v.items():
                    valid_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates if not pd.isna(date)]
                    if valid_dates:
                        min_date[k].append(min(valid_dates))
            res_df['all_cause_death_icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'all_cause_death_icd10_date': [min(v) for v in min_date.values()]})

        # Process visit dates similarly to the original function
        if 'visit_dates' in self.event_data:
            print("Processing visit dates...")
            visit_dates = self.event_data['visit_dates'].reset_index()
            visit_dates.rename(columns={
                'eid': 'feid',
                '53-0.0': "Baseline_visit_date",
                '53-1.0': "Calibration_visit_date",
                '53-2.0': "Imaging_visit_date1",
                '53-3.0': "Imaging_visit_date2"
            }, inplace=True)
            res_df['visit_dates'] = visit_dates

        # Combining results from different categories
        print("Combining results from different categories...")
        combined_df = pd.DataFrame()
        for key, df in res_df.items():
            if not df.empty:
                df.set_index('feid', inplace=True)
                combined_df = pd.concat([combined_df, df], axis=1)

        print('Printing first 20 rows of combined data:')
        print(combined_df.head(20))

        print("Event search completed.")
        return combined_df.reset_index()

# Note: The instantiation of the class and the method call would require actual 'event_data' and 'event_organiser' objects.

import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
from event_code_search.modules.dataorganiser import DataOrganiser

class EventSearcher(DataOrganiser):
    def __init__(self, event_data, output_path, output_filename):
        super().__init__(event_data)
        self.output_path = output_path
        self.output_filename = output_filename
        self.issues_log = []

    def search_events(self, icd10_codes=None, icd9_codes=None, death_icd10_codes=None, opcs4_codes=None, 
                    all_causes_death=False):

        if icd10_codes:
            icd10_dict = self.organiser('icd10')
            print('Organiser ran for icd10_dict')
        if icd9_codes:
            icd9_dict = self.organiser('icd9')
        if death_icd10_codes:
            death_icd10_dict = self.organiser('death_icd10')
        if opcs4_codes:
            opcs4_dict = self.organiser('opcs4') 
        
        res_df = dict.fromkeys(['icd10', 'icd9', 'death_icd10', 'opcs4', 'visit_dates'])

        visit_dates = self.event_data['visit_dates'].reset_index()
        visit_dates.rename(columns={'eid':'feid',
                                    '53-0.0':"Baseline_visit_date", 
                                    '53-1.0':"Calibration_visit_date", 
                                    '53-2.0':"Imaging_visit_date1", 
                                    '53-3.0':"Imaging_visit_date2",}, inplace=True)
        res_df['visit_dates'] = visit_dates
        
        if icd10_codes:
            min_date = defaultdict(list)
            for k, v in icd10_dict.items():
                for icd, date in v.items():
                    #if icd in icd10_codes:
                    if any(icd.startswith(s) for s in icd10_codes): #If string starts with icd code
                        #min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        if pd.isna(date[0]): #Added on 13/13/2023 - some missing year values
                            print("Problem here!!!", k, icd, date) #Remove this individual
                            continue
                            #fake_date = '1970-01-01' #Add a random prevalent date
                            #min_date[k].append(datetime.strptime(fake_date, '%Y-%m-%d').date())
                        min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        #print(min_date[k])
                        #min_date[k] = sorted(min_date[k], key=lambda tup: tup[0])
            for k, v in min_date.items():
                min_date[k] = np.min(v)
            feid_list = list(min_date.keys())
            dx_date_list = [min_date[k] for k in feid_list]
            res_df['icd10'] = pd.DataFrame({'feid':feid_list, 'icd10_dx_date':dx_date_list})
        
        if icd9_codes:
            min_date = defaultdict(list)
            for k, v in icd9_dict.items():
                for icd, date in v.items():
                    #if icd in icd9_codes:
                    if any(icd.startswith(s) for s in icd9_codes): #If string starts with icd code
                        if pd.isna(date[0]): #Added on 13/13/2023 - some missing year values
                            print("Problem here!!!", k, icd, date) #Remove this individual
                            continue
                            #fake_date = '1970-01-01' #Add a random prevalent date
                            #min_date[k].append(datetime.strptime(fake_date, '%Y-%m-%d').date())
                        min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        #print(min_date[k])
                        #min_date[k] = sorted(min_date[k], key=lambda tup: tup[0])
            for k, v in min_date.items():
                min_date[k] = np.min(v)
            feid_list = list(min_date.keys())
            dx_date_list = [min_date[k] for k in feid_list]
            res_df['icd9'] = pd.DataFrame({'feid':feid_list, 'icd9_dx_date':dx_date_list})

        if death_icd10_codes:
            min_date = defaultdict(list)
            for k, v in death_icd10_dict.items():
                for icd, date in v.items():
                    #if icd in death_icd10_codes:
                    if any(icd.startswith(s) for s in death_icd10_codes): #If string starts with icd code
                        if pd.isna(date[0]): #Added on 13/13/2023 - some missing year values
                            print("Problem here!!!", k, icd, date) #Remove this individual
                            continue
                            #fake_date = '1970-01-01' #Add a random prevalent date
                            #min_date[k].append(datetime.strptime(fake_date, '%Y-%m-%d').date())
                        min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        #print(min_date[k])
                        #min_date[k] = sorted(min_date[k], key=lambda tup: tup[0])
            for k, v in min_date.items():
                min_date[k] = np.min(v)
            feid_list = list(min_date.keys())
            dx_date_list = [min_date[k] for k in feid_list]
            res_df['death_icd10'] = pd.DataFrame({'feid':feid_list, 'death_icd10_date':dx_date_list})
        
        if all_causes_death:
            min_date = defaultdict(list)
            for k, v in death_icd10_dict.items():
                for icd, date in v.items():
                    if icd: #If icd is a string
                        if pd.isna(date[0]): #Added on 13/13/2023 - some missing year values
                            print("Problem here!!!", k, icd, date) #Remove this individual
                            continue
                        min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        #print(min_date[k])
                        #min_date[k] = sorted(min_date[k], key=lambda tup: tup[0])
            for k, v in min_date.items():
                min_date[k] = np.min(v)
            feid_list = list(min_date.keys())
            dx_date_list = [min_date[k] for k in feid_list]
            res_df['all_cause_death_icd10'] = pd.DataFrame({'feid':feid_list, 'all_cause_death_icd10_date':dx_date_list})
            
        if opcs4_codes:
            min_date = defaultdict(list)
            for k, v in opcs4_dict.items():
                for icd, date in v.items():
                    #if icd in opcs4_codes:
                    if any(icd.startswith(s) for s in opcs4_codes): #If string starts with icd code
                        if pd.isna(date[0]): #Added on 13/13/2023 - some missing year values
                            print("Problem here!!!", k, icd, date) #Remove this individual
                            continue
                        min_date[k].append(datetime.strptime(date[0], '%Y-%m-%d').date())
                        #print(min_date[k])
                        #min_date[k] = sorted(min_date[k], key=lambda tup: tup[0])
            for k, v in min_date.items():
                min_date[k] = np.min(v)
            feid_list = list(min_date.keys())
            dx_date_list = [min_date[k] for k in feid_list]
            res_df['opcs4'] = pd.DataFrame({'feid':feid_list, 'opcs4_date':dx_date_list})

        res_df = {k: v for k, v in res_df.items() if v is not None}
        res_df = {k:v.set_index('feid') for k, v in res_df.items()}   
        res_df = pd.concat(res_df, axis=1)
        res_df.columns = res_df.columns.droplevel(0)
        res_df.reset_index(inplace=True)
        
        return res_df


"""
    def log_issue(self, feid, code, dates):
        message = f"Problem here!!! {feid} {code} {dates}"
        self.issues_log.append(message)

    def process_events(self, event_dict, codes, code_type):
        min_date = defaultdict(list)
        for k, v in event_dict.items():
            for icd, dates in v.items():
                if any(icd.startswith(code) for code in codes):
                    if pd.isna(dates[0]):
                        self.log_issue(k, icd, dates)
                        continue
                    try:
                        valid_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates if pd.notna(date)]
                        min_date[k].append(min(valid_dates))
                    except ValueError as e:
                        self.log_issue(k, icd, f"Date format error: {e}")
        return min_date

    def save_issues_log(self):
        if self.issues_log:
            base_name = os.path.splitext(os.path.basename(self.output_filename))[0]
            issues_filename = f"{base_name}_IDs_with_Issues.txt"
            issues_path = os.path.join(self.output_path, issues_filename)
            with open(issues_path, "w") as file:
                for message in self.issues_log:
                    file.write(message + "\n")
            print(f"Issues log saved to {issues_path}")

    def search_events(self, icd10_codes=None, icd9_codes=None, death_icd10_codes=None, opcs4_codes=None, icd10=False, icd9=False, death_icd10=False, opcs4=False, all_causes_death=False):
        print("Starting search for events...")
        res_df = defaultdict(pd.DataFrame)

        if 'visit_dates' in self.event_data:
            visit_dates = self.event_data['visit_dates'].rename(columns={
                'eid': 'feid',
                '53-0.0': "Baseline_visit_date",
                '53-1.0': "Calibration_visit_date",
                '53-2.0': "Imaging_visit_date1",
                '53-3.0': "Imaging_visit_date2",
            })
            res_df['visit_dates'] = visit_dates

        if icd10_codes:
            icd10_dict = self.data_organiser.organiser('icd10')
            min_date = self.process_events(icd10_dict, icd10_codes, 'ICD-10')
            res_df['icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'icd10_dx_date': [min(v) for v in min_date.values()]}).drop_duplicates()

        if icd9_codes:
            icd9_dict = self.data_organiser.organiser('icd9')
            min_date = self.process_events(icd9_dict, icd9_codes, 'ICD-9')
            res_df['icd9'] = pd.DataFrame({'feid': list(min_date.keys()), 'icd9_dx_date': [min(v) for v in min_date.values()]}).drop_duplicates()

        if death_icd10_codes:
            death_icd10_dict = self.data_organiser.organiser('death_icd10')
            min_date = self.process_events(death_icd10_dict, death_icd10_codes, 'Death ICD-10')
            res_df['death_icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'death_icd10_date': [min(v) for v in min_date.values()]}).drop_duplicates()

        if opcs4_codes:
            opcs4_dict = self.data_organiser.organiser('opcs4')
            min_date = self.process_events(opcs4_dict, opcs4_codes, 'OPCS-4')
            res_df['opcs4'] = pd.DataFrame({'feid': list(min_date.keys()), 'opcs4_date': [min(v) for v in min_date.values()]}).drop_duplicates()

        if all_causes_death:
            # Assuming all death codes are relevant for all-cause mortality, no specific codes to filter
            death_dict = self.data_organiser.organiser('death_icd10')
            min_date = self.process_events(death_dict, [], 'All Causes Death')
            res_df['all_cause_death_icd10'] = pd.DataFrame({'feid': list(min_date.keys()), 'all_cause_death_icd10_date': [min(v) for v in min_date.values()]}).drop_duplicates()

        res_df = {k: v for k, v in res_df.items() if v is not None}
        res_df = {k:v.set_index('feid') for k, v in res_df.items()}   
        res_df = pd.concat(res_df, axis=1)
        res_df.columns = res_df.columns.droplevel(0)
        res_df.reset_index(inplace=True)

        print('Printing first 20 rows of combined dataframe from event search:')
        print(res_df.head(20))
    
        self.save_issues_log()
        print("Event search completed.")
        return res_df
"""
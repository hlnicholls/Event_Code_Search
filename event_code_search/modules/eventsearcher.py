import pandas as pd
import numpy as np
from datetime import datetime
from collections import defaultdict
from event_code_search.modules.dataorganiser import DataOrganiser

class EventSearcher(DataOrganiser):
    """
    Inherits from DataOrganiser to search for medical events based on specific criteria 
    like ICD codes and all-causes of death within the provided event data.

    Attributes:
        event_data (dict): Preloaded event data.
        output_path (Path): The path where output files will be saved.
        output_filename (str): The name of the output file.
        issues_log (list): Logs issues encountered during event search.

    Methods:
        __init__(self, event_data, output_path, output_filename):
            Initializes the EventSearcher with event data, output path, and filename.
            
        search_events(self, icd10_codes=None, icd9_codes=None, death_icd10_codes=None, 
                      opcs4_codes=None, all_causes_death=False):
            Searches for events based on the specified ICD10, ICD9, death-related ICD10, 
            OPCS4 codes, and includes all causes of death if specified. It organizes 
            the results into a structured format for output.
            
            Arguments:
                icd10_codes (list[str], optional): List of ICD-10 codes to filter events.
                icd9_codes (list[str], optional): List of ICD-9 codes to filter events.
                death_icd10_codes (list[str], optional): List of death-related ICD-10 codes 
                                                         to filter events.
                opcs4_codes (list[str], optional): List of OPCS4 codes to filter events.
                all_causes_death (bool, optional): Flag to include all-cause mortality in the search.
                
            Returns:
                pd.DataFrame: A DataFrame with the search results organized by the specified 
                              criteria, including event dates and types.
    """
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
            print('Organiser ran for icd9_dict')
        if death_icd10_codes:
            death_icd10_dict = self.organiser('death_icd10')
            print('Organiser ran for death_icd10_dict')
        if opcs4_codes:
            opcs4_dict = self.organiser('opcs4') 
            print('Organiser ran for opcs4_dict')
        
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
            print("Note: all-causes-death flag must also have icd10-death-codes defined")
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

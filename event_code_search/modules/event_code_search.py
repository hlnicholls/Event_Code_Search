import os, re, sys
from collections import defaultdict
from pprint import pprint
import pandas as pd
import numpy as np
from datetime import datetime
from natsort import natsorted
import pyreadr
import pickle as pkl
import os
import copy

#Set RunID 
run_ID = 'ID47535'
#dat path changed to data downloaded from DNAnexus - done on 12/12/2023
dat_path = '/raid/projects/Outcome_data_search/Input/outcome_data_all_20231212.csv'
#header_path = '/raid/genetics/ukb_decoded_data/Input/' + run_ID + '/'+ 'header_transformed.rds'

dat = pd.read_csv(dat_path, low_memory=False)

headers = pd.DataFrame({"UDI":dat.columns})


#Problematic case eid = 2613314
#The list of ICD10 codes do not match with the ones shown in DNAnexus cohort browser
dat_2613314 = dat[dat.eid==2613314]

#Prepare the input data, needs to be done only once
#headers = pyreadr.read_r(header_path)[None]

icd10_cols = [i for i in headers.UDI if i.startswith('41270')]
icd10_date_cols = [i for i in headers.UDI if i.startswith('41280')]
icd9_cols = [i for i in headers.UDI if i.startswith('41271')]
icd9_date_cols = [i for i in headers.UDI if i.startswith('41281')]
opcs4_cols = [i for i in headers.UDI if i.startswith('41272')]
opcs4_date_cols = [i for i in headers.UDI if i.startswith('41282')]
death_icd10_cols = [i for i in headers.UDI if i.startswith('40001')]
death_icd10_date_cols = [i for i in headers.UDI if i.startswith('40000')]
visit_date_cols = [i for i in headers.UDI if i.startswith('53-')]


#Sense check - all output should be true
if (len(icd10_cols) == len(icd10_date_cols)) & (len(icd9_cols) == len(icd9_date_cols)) & (len(opcs4_cols) == len(opcs4_date_cols)) & (len(death_icd10_cols) == len(death_icd10_date_cols)):
    icd10_dat = pd.read_csv(dat_path, usecols=['eid']+icd10_cols, low_memory=False)
    icd10_dates_dat = pd.read_csv(dat_path, usecols=['eid']+icd10_date_cols, low_memory=False)
    icd9_dat = pd.read_csv(dat_path, usecols=['eid']+icd9_cols, low_memory=False)
    icd9_dates_dat = pd.read_csv(dat_path, usecols=['eid']+icd9_date_cols, low_memory=False)
    opcs4_dat = pd.read_csv(dat_path, usecols=['eid']+opcs4_cols, low_memory=False)
    opcs4_dates_dat = pd.read_csv(dat_path, usecols=['eid']+opcs4_date_cols, low_memory=False)
    death_icd10_dat = pd.read_csv(dat_path, usecols=['eid']+death_icd10_cols, low_memory=False)
    death_icd10_dates_dat = pd.read_csv(dat_path, usecols=['eid']+death_icd10_date_cols, low_memory=False)
    visit_dates_dat = pd.read_csv(dat_path, usecols=['eid']+visit_date_cols, low_memory=False)
    
    event_data = {'icd10':icd10_dat, 'icd10_dates':icd10_dates_dat,
          'icd9':icd9_dat, 'icd9_dates':icd9_dates_dat,
          'opcs4':opcs4_dat, 'opcs4_dates':opcs4_dates_dat,
          'death_icd10':death_icd10_dat, 'death_icd10_dates':death_icd10_dates_dat,
         'visit_dates':visit_dates_dat}
    
    #with open(' ' + run_ID + '/' + 'event_data_' + run_ID + '.pkl', 'wb') as f:
    with open('/raid/projects/Outcome_data_search/Input/event_data_20231212.pkl', 'wb') as f:
        pkl.dump(event_data, f)
        
else:
    print('There is something wrong with the input data.')


with open('/raid/projects/Outcome_data_search/Input/event_data_20231212.pkl', 'rb') as f:
    event_data = pkl.load(f)
    

#Organise ICD10, ICD9, Death_ICD10 and OPCS4 data

def organiser(event_type):
    
    #Helper function
    def isnan(x):
        try:
            y = np.isnan(x)
        except:
            y = False
        return y

    def notnan(x):
        return not(isnan(x))
    
    df_codes = event_data[event_type]
    df_dates = event_data[event_type+ '_dates']
    df_codes.index = df_codes['eid']
    df_dates.index = df_dates['eid']
    df_codes = df_codes.reindex(natsorted(df_codes.columns), axis=1)
    df_dates = df_dates.reindex(natsorted(df_dates.columns), axis=1)

    dct_dates_feid_then_icd = {}
    n = 0
    for (cnd, date_list), (cnc, icd_list) in zip(df_dates.T.items(), df_codes.T.items()):
        n = n + 1
        assert cnd == cnc
        feid = cnd
        dct = defaultdict(list)
        del date_list['eid']
        del icd_list['eid']


        ## Makes an ordering assumption
        #icd_list_notnan = [x for x in icd_list if notnan(x)]
        #sicd = icd_list_notnan
        #for x in icd_list_notnan:
        #    m = icd_list_notnan.count(x)
        #    if m>1:
        #        print(x, m)
        #        raise Exception("Don't expect this to happen")


        #nicd = len(icd_list_notnan)

        for dt, icd in zip(date_list, icd_list):
            if isnan(icd):
                break # this is a break and not a pass as the data is ordered; once a nan always an nan
            else:
                dct[icd].append(dt) 

        if not dct:
            continue
        dct_dates_feid_then_icd[feid] = dict(dct)
    
    return dct_dates_feid_then_icd


#Get dictionaries of outcomes
icd10_dict = organiser('icd10')
icd9_dict = organiser('icd10')
death_icd10_dict = organiser('death_icd10')
opcs4_dict = organiser('opcs4')


#Add all-cause mortality N searcher

def event_search(icd10_codes=None, icd9_codes=None, death_icd10_codes=None, opcs4_codes=None, 
                 icd10=False, icd9=False, death_icd10=False, opcs4=False, all_causes_death=False):    
    
    res_df = dict.fromkeys(['icd10', 'icd9', 'death_icd10', 'opcs4', 'visit_dates'])
    
    visit_dates = event_data['visit_dates'].reset_index()
    visit_dates.rename(columns={'eid':'feid',
                                '53-0.0':"Baseline_visit_date", 
                                '53-1.0':"Calibration_visit_date", 
                                '53-2.0':"Imaging_visit_date1", 
                                '53-3.0':"Imaging_visit_date2",}, inplace=True)
    res_df['visit_dates'] = visit_dates
    
    if icd10:
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
    
    if icd9:
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

    if death_icd10:
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
        
    if opcs4:
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


#Read in the ICD10 previously prepared by Hafiz and Nay
dat_path = '/raid/projects/Collaborations/Pankaj_Garg/LVFP/Input'
icd10 = pd.read_excel(os.path.join(dat_path, 'ICD10_coding_for_Hafiz_NA.xlsx'))

#MACE events column
mace = icd10.loc[:, ['coding', 'Ischaemic', 'MI']]
mace_filtered = mace[mace.applymap(lambda x: x==1).any(1)].coding.tolist()

#HF from Elisa (no cardiomyopathy)
hf_icd10 = ['I500', 'I501', 'I509', 'I110', 'I130', 'I132', 'I255', 'K761', 'J81']

#MACE including HF
mace_plus_hf = mace_filtered + hf_icd10

#Ventricular arrhythmia
va = icd10.loc[:, ['coding', 'VF', 'VT']]
va_filtered = va[va.applymap(lambda x: x==1).any(1)].coding.tolist()

#HCM
hcm_icd10 = ['I421', 'I422']
hcm_icd9 = ['4251']

#DCM
dcm_icd10 = ['I420']

#Hypertensive heart disease
hhd_icd10 = ['I110', 'I119', 'I130', 'I131', 'I132', 'I139']

dat_path2 = '/raid/projects/Collaborations/Kat_Gilbert/Input'
opcs4 = pd.read_excel(os.path.join(dat_path2, 'OPCS4_header_formatted.xlsx'))
opcs4_selected = opcs4.loc[:,['coding', 
       'Left heart cath', 'Right heart cath', 'Left & right cath',
       'Left heart cath+balloon/stent', 'Pacemaker', 'ICD', 'Valve repair',
       'Valve replacement', 'CABG']]

#AF events column
af = icd10.loc[:, ['coding', 'AF']]
af_filtered = af[af.applymap(lambda x: x==1).any(1)].coding.tolist()
af_filtered = af_filtered + ['I489'] #Add I48.9 Atrial fibrillation and atrial flutter, unspecified

af_opcs4 = ['K621']
'''
icd10_selected = icd10.loc[:, ['Coding', 'Hypertension', 'Diabetes',
       'High cholesterol', 'Obesity', 'AF', 'VF', 'VT', 'Ischaemic',
       'Haemorrhagic', 'Stable Angina', 'Unstable angina', 'MI', 'Ischaemic.1',
       'DCM', 'Alcoholic', 'HCM']]

opcs4 = pd.read_excel(os.path.join(dat_path, 'OPCS4_header_formatted.xlsx'))
opcs4_selected = opcs4.loc[:,['coding', 
       'Left heart cath', 'Right heart cath', 'Left & right cath',
       'Left heart cath+balloon/stent', 'Pacemaker', 'ICD', 'Valve repair',
       'Valve replacement', 'CABG']]
'''

mace_events = event_search(icd10_codes=mace_filtered, 
                           death_icd10_codes=mace_filtered,
                           icd10=True, death_icd10=True)

mace_plus_hf_events = event_search(icd10_codes=mace_plus_hf, 
                                   death_icd10_codes=mace_plus_hf,
                                   icd10=True, death_icd10=True)

hf_events = event_search(icd10_codes=hf_icd10, 
                         death_icd10_codes=hf_icd10,
                         icd10=True, death_icd10=True)


va_events = event_search(icd10_codes=va_filtered, 
                         death_icd10_codes=va_filtered,
                         icd10=True, death_icd10=True)

all_cause_mortality = event_search(all_causes_death=True)


#Composite end-point = mace_plus_hf + va + all-cause mortality
composite_events = event_search(icd10_codes=mace_plus_hf+va_filtered, 
                                death_icd10_codes=mace_plus_hf+va_filtered,
                                icd10=True, death_icd10=True, all_causes_death=True)

hcm_events = event_search(icd10_codes=hcm_icd10, 
                         death_icd10_codes=hcm_icd10,
                          icd9_codes=hcm_icd9,
                         icd10=True, icd9=True, death_icd10=True)

dcm_events = event_search(icd10_codes=dcm_icd10, 
                         death_icd10_codes=dcm_icd10,
                         icd10=True, icd9=False, death_icd10=True)

hhd_events = event_search(icd10_codes=hhd_icd10, 
                         death_icd10_codes=hhd_icd10,
                         icd10=True, icd9=False, death_icd10=True)

af_events = event_search(icd10_codes=af_filtered, 
                           death_icd10_codes=af_filtered,
                           icd10=True, death_icd10=True, opcs4_codes=af_opcs4, opcs4=True)
#Organise output into Pandas format
def output_organiser(dataset, all_cause_mortality_only=False):
    dataset_final_final2 = copy.deepcopy(dataset)
    col_list = dataset_final_final2.columns.tolist()
    col_list_dates = [k for k in col_list if 'date' in k]
    for i in col_list_dates:
        dataset_final_final2[i] = pd.to_datetime(dataset_final_final2[i])
    visit_dates = ['Baseline_visit_date', 'Calibration_visit_date', 'Imaging_visit_date1', 'Imaging_visit_date2']
    col_list_dates_relevant = [name for name in col_list_dates if not any(substring in name for substring in visit_dates)]
    dataset_final_final2['Event_date'] = dataset_final_final2[col_list_dates_relevant].min(axis=1)
    dataset_final_final2 = dataset_final_final2.loc[:, ['feid']+visit_dates+['Event_date']]

    return dataset_final_final2


res_list_final ={'mace_events':mace_events, 
                 'mace_plus_hf_events':mace_plus_hf_events, 'hf_events':hf_events, 
                 'all_cause_mortality':all_cause_mortality}

res_df_final = {}

for k in res_list_final.keys():
    print(k)
    res_df_final[k] = output_organiser(res_list_final[k])



for i in res_df_final.keys():
    print(i)
    print(res_df_final[i]['Event_date'].isnull().value_counts())


outpath = '/raid/projects/Heart_Kidney_Project/LVphenotypes_CKD/Input/'
for k in res_df_final.keys():
    print(k)
    res_df_final[k].to_csv(outpath+k+'18122023.csv', index=False)
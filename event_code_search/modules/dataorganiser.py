import numpy as np
from collections import defaultdict
from natsort import natsorted

class DataOrganiser:
    def __init__(self, event_data):
        self.event_data = event_data

    def isnan(self, x):
        try:
            y = np.isnan(x)
        except:
            y = False
        return y

    def notnan(self, x):
        return not(self.isnan(x))

    def organiser(self, event_type):
        print('Organising event codes and dates...')
        df_codes = self.event_data[event_type]
        df_dates = self.event_data[event_type + '_dates']
        df_codes.index = df_codes['eid']
        df_dates.index = df_dates['eid']
        df_codes = df_codes.reindex(natsorted(df_codes.columns), axis=1)
        df_dates = df_dates.reindex(natsorted(df_dates.columns), axis=1)

        dct_dates_feid_then_icd = {}
        for (cnd, date_list), (cnc, icd_list) in zip(df_dates.T.items(), df_codes.T.items()):
            assert cnd == cnc
            feid = cnd
            dct = defaultdict(list)
            del date_list['eid']
            del icd_list['eid']

            for dt, icd in zip(date_list, icd_list):
                if self.isnan(icd):
                    break
                else:
                    dct[icd].append(dt)

            if not dct:
                continue
            dct_dates_feid_then_icd[feid] = dict(dct)
        print('Printing first 5 key value pairs of organised data dictionary:')
        for i, (key, value) in enumerate(dct_dates_feid_then_icd.items()):
            print(key, value)
            if i == 4:  # Stops after printing 5 items (0 to 4)
                break
        return dct_dates_feid_then_icd

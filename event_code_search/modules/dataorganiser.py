import numpy as np
from collections import defaultdict
from natsort import natsorted

class DataOrganiser:
    """
    Organizes event data based on specific event types, such as ICD codes, and their corresponding dates.

    Attributes:
        event_data (dict): Contains the preloaded event data with keys representing event types and values 
                           being DataFrames of codes and dates.

    Methods:
        __init__(self, event_data):
            Initializes the DataOrganiser with event data.

            Arguments:
                event_data (dict): The preloaded event data.

        organiser(self, event_type):
            Organizes event data by sorting and aligning event codes with their corresponding dates, based 
            on the specified event type.

            This method assumes the event data is structured with separate DataFrames for event codes and 
            event dates, indexed by a unique event identifier (eid). It returns a dictionary mapping each 
            eid to another dictionary, where each key is an event code and the value is a list of dates 
            associated with that event.

            Arguments:
                event_type (str): The type of event to organize. Expected to correspond to keys in the 
                                  event_data dictionary, with a suffix of '_dates' for date data.

            Returns:
                dict: A nested dictionary where the first level keys are eids, and the second level keys 
                      are event codes with their associated dates as values.

            The method includes helper functions:
                isnan(x): Checks if the input is NaN (Not a Number).
                notnan(x): Checks if the input is not NaN.
    """
    def __init__(self, event_data):
        self.event_data = event_data

    def organiser(self, event_type):
        
        #Helper function
        def isnan(x):
            try:
                y = np.isnan(x)
            except:
                y = False
            return y

        def notnan(x):
            return not(isnan(x))
        
        df_codes = self.event_data[event_type]
        df_dates = self.event_data[event_type+ '_dates']
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
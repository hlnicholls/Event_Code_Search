import pandas as pd
import copy

class OutputOrganiser:
    @staticmethod
    def organise_output(dataset, all_cause_mortality_only=False):
        dataset_final_final2 = copy.deepcopy(dataset)
        col_list = dataset_final_final2.columns.tolist()
        col_list_dates = [k for k in col_list if 'date' in k]
        for i in col_list_dates:
            dataset_final_final2[i] = pd.to_datetime(dataset_final_final2[i])
        visit_dates = ['Baseline_visit_date', 'Calibration_visit_date', 'Imaging_visit_date1', 'Imaging_visit_date2']
        col_list_dates_relevant = [name for name in col_list_dates if not any(substring in name for substring in visit_dates)]
        print(col_list_dates)
        print(col_list_dates_relevant)
        dataset_final_final2['Event_date'] = dataset_final_final2[col_list_dates_relevant].min(axis=1)
        dataset_final_final2 = dataset_final_final2.loc[:, ['feid']+visit_dates+['Event_date']]
        dataset_final_final2 = dataset_final_final2.sort_values(by='feid', ascending=True)
        print('Head of final dataframe:')
        print(dataset_final_final2.head(5))
        return dataset_final_final2



    """
    def organise_output(dataset, all_cause_mortality_only=False):
        print("Starting output organisation...")
        
        dataset_copy = copy.deepcopy(dataset)

        for column in dataset_copy.columns:
            if 'date' in column and dataset_copy[column].dtype == object:
                dataset_copy[column] = pd.to_datetime(dataset_copy[column], errors='coerce')
        print("Date columns converted to datetime format.")

        # Identify all date columns related to events, excluding visit dates
        event_date_columns = [col for col in dataset_copy.columns if 'date' in col and 'visit' not in col]

        # Calculate the earliest event date from the relevant event date columns
        dataset_copy['Event_date'] = dataset_copy[event_date_columns].min(axis=1)
        print("Earliest event date calculated across all relevant event dates.")

        # Optionally filter for all-cause mortality only
        if all_cause_mortality_only:
            #TODO Adjust logic to focus on all-cause mortality dates only
            print("Filtering for all-cause mortality only.")
            # This would be customized based on your dataset's structure

        final_columns = ['feid', 'Baseline_visit_date', 'Calibration_visit_date', 'Imaging_visit_date1', 'Imaging_visit_date2', 'Event_date']
        dataset_final = dataset_copy.loc[:, final_columns]
        print("Output organisation completed.")
        return dataset_final
"""
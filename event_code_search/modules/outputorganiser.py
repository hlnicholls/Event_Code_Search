import pandas as pd
import copy

class OutputOrganiser:
    @staticmethod
    def organise_output(dataset, all_cause_mortality_only=False):
        print("Starting output organisation...")
        
        # Deep copy the dataset to avoid modifying the original data
        dataset_copy = copy.deepcopy(dataset)
        print("Dataset copied for modification.")
        
        # Ensure all date columns are in datetime format
        for column in dataset_copy.columns:
            if 'date' in column and dataset_copy[column].dtype == object:
                dataset_copy[column] = pd.to_datetime(dataset_copy[column], errors='coerce')
        print("Date columns converted to datetime format.")

        # Filter columns to include only those relevant for all-cause mortality if specified
        if all_cause_mortality_only:
            print("Filtering for all-cause mortality only.")
            relevant_columns = [col for col in dataset_copy.columns if 'all_cause_death' in col]
            dataset_copy = dataset_copy[relevant_columns + ['feid']]

        # Find the earliest event date across relevant columns
        date_columns = [col for col in dataset_copy.columns if 'date' in col]
        dataset_copy['Earliest_Event_Date'] = dataset_copy[date_columns].min(axis=1)
        print("Earliest event date calculated.")

        # Prepare for selecting relevant columns for the final output
        visit_dates = ['Baseline_visit_date', 'Calibration_visit_date', 'Imaging_visit_date1', 'Imaging_visit_date2']
        final_columns = ['feid'] + visit_dates + ['Earliest_Event_Date']
        
        # Check if the expected columns exist before attempting to access them
        existing_columns = [col for col in final_columns if col in dataset_copy.columns]
        if len(existing_columns) != len(final_columns):
            missing_cols = set(final_columns) - set(existing_columns)
            print(f"Warning: Expected columns {missing_cols} are missing in the dataset.")
        
        final_dataset = dataset_copy.loc[:, existing_columns].dropna(subset=['Earliest_Event_Date'])
        print("Final dataset organised and ready.")

        return final_dataset

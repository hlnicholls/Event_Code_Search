# Adjust imports according to your package structure
#from event_code_search.modules.dataorganiser import DataOrganiser
from event_code_search.modules.eventsearcher import EventSearcher
from event_code_search.modules.outputorganiser import OutputOrganiser
from event_code_search.config_class import Config  # Import the Config class
import pickle as pkl

def main():
    """
    Searching medical event data based on user-specified criteria.

    Arguments:
        --pkl_path (Path): Required. The path to the pickle file containing preloaded event data.
        --output_path (Path): Required. The directory path where the output files will be saved.
        --output_filename (str): Required. The filename for the output CSV file.
        --icd10_codes (list[str]): Optional. A list of ICD-10 codes or a path to a text file containing these codes,
                                used to filter events.
        --icd9_codes (list[str]): Optional. A list of ICD-9 codes or a path to a text file containing these codes,
                                used to filter events.
        --death_icd10_codes (list[str]): Optional. A list of death-related ICD-10 codes or a path to a text file
                                        containing these codes, used to filter events.
        --opcs4_codes (list[str]): Optional. A list of OPCS-4 codes or a path to a text file containing these codes,
                                used to filter events.
        --all_causes_death (bool): Optional. A flag indicating whether to include all-cause mortality in the search.

    Methods:
        Config.create_from_args():
            Parses the command-line arguments to create a configuration object for the application.

        EventSearcher.search_events():
            Uses the provided ICD codes and flags to search through the preloaded event data and identify relevant
            medical events.

        OutputOrganiser.organise_output():
            Takes the results of the event search and organizes them into a structured format suitable for output,
            including calculating and formatting dates and event categories.
    """

    cfg = Config.create_from_args()  

    print('Reading in event data...')
    with open(cfg.pkl_path, 'rb') as f:
        event_data = pkl.load(f)

    event_searcher = EventSearcher(event_data, cfg.output_path, cfg.output_filename) 
    events_result = event_searcher.search_events(
        icd10_codes=cfg.icd10_codes,
        icd9_codes=cfg.icd9_codes,
        death_icd10_codes=cfg.death_icd10_codes,
        opcs4_codes=cfg.opcs4_codes,
        all_causes_death=cfg.all_causes_death
    )

    res_list_final ={'events':events_result}
    final_output_path = cfg.output_path / cfg.output_filename 
    res_df_final = {}

    for k in res_list_final.keys():
        print(k)
        res_df_final[k] = OutputOrganiser.organise_output(res_list_final[k])

    for i in res_df_final.keys():
        print(i)
        print(res_df_final[i]['Event_date'].isnull().value_counts())

    for k in res_df_final.keys():
        print(k)
        res_df_final[k].to_csv(final_output_path, index=False)

if __name__ == "__main__":
    main()

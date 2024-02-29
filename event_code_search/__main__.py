# Adjust imports according to your package structure
from event_code_search.modules.dataloader import DataLoader
#from event_code_search.modules.dataorganiser import DataOrganiser
from event_code_search.modules.eventsearcher import EventSearcher
from event_code_search.modules.outputorganiser import OutputOrganiser
from event_code_search.config_class import Config  # Import the Config class
import pickle as pkl

def main():
    cfg = Config.create_from_args()  # Instantiate Config with command-line arguments

    # Load and prepare the data
    #data_loader = DataLoader(cfg.dat_path)
    #data_loader.load_outcome_data()
    #data_loader.load_event_data(cfg.pkl_path)

    #dat = pd.read_csv(cfg.dat_path, low_memory=False)
    print('Reading in event data...')
    with open(cfg.pkl_path, 'rb') as f:
        event_data = pkl.load(f)

    # Organise the event data
    #data_organiser = DataOrganiser(data_loader.event_data)

    # Search for events based on user-specified ICD codes and flags
    # Now passing output_path and output_filename to EventSearcher
    event_searcher = EventSearcher(event_data, cfg.output_path, cfg.output_filename) #data_organiser, 
    events_result = event_searcher.search_events(
        icd10_codes=cfg.icd10_codes,
        icd9_codes=cfg.icd9_codes,
        death_icd10_codes=cfg.death_icd10_codes,
        opcs4_codes=cfg.opcs4_codes,
        all_causes_death=cfg.all_causes_death
    )

    # Organise and output the final results
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

    #final_data = OutputOrganiser.organise_output(events_result)
    #final_output_path = cfg.output_path / cfg.output_filename 
    #final_data.to_csv(final_output_path, index=False)

if __name__ == "__main__":
    main()

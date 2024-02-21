import argparse
from pathlib import Path
import os

class Config:
    def __init__(self, dat_path, pkl_path, output_path, icd10_codes=[], icd9_codes=[], death_icd10_codes=[], opcs4_codes=[], all_causes_death=False):
        self.dat_path = dat_path
        self.pkl_path = pkl_path
        self.output_path = output_path
        self.icd10_codes = icd10_codes
        self.icd9_codes = icd9_codes
        self.death_icd10_codes = death_icd10_codes
        self.opcs4_codes = opcs4_codes
        self.all_causes_death = all_causes_death

        try:
            os.makedirs(self.output_path, exist_ok=True)
        except FileExistsError:
            pass


    @staticmethod
    def create_from_args():
        parser = argparse.ArgumentParser(description="Process and analyze medical event data.")
        parser.add_argument('--dat_path', type=Path, required=True, help='Path to the CSV data file containing the dataset.')
        parser.add_argument('--pkl_path', type=Path, required=True, help='Path to the pickle file containing preloaded event data.')
        parser.add_argument('--output_path', type=Path, required=True, help='Directory path for saving the output files.')
        parser.add_argument('--icd10_codes', type=str, nargs='+', default=[], help='List of ICD10 codes of interest. Space-separated if multiple.')
        parser.add_argument('--icd9_codes', type=str, nargs='+', default=[], help='List of ICD9 codes of interest. Space-separated if multiple.')
        parser.add_argument('--death_icd10_codes', type=str, nargs='+', default=[], help='List of Death-related ICD10 codes of interest. Space-separated if multiple.')
        parser.add_argument('--opcs4_codes', type=str, nargs='+', default=[], help='List of OPCS4 codes of interest. Space-separated if multiple.')
        parser.add_argument('--all_causes_death', action='store_true', help='Flag to include all-cause mortality in the search.')
        args = parser.parse_args()

        return Config(
            dat_path=args.dat_path, pkl_path=args.pkl_path, output_path=args.output_path,
            icd10_codes=args.icd10_codes, icd9_codes=args.icd9_codes,
            death_icd10_codes=args.death_icd10_codes, opcs4_codes=args.opcs4_codes,
            all_causes_death=args.all_causes_death
        )

import argparse
from pathlib import Path
import os

class Config:
    def __init__(self, pkl_path, output_path, output_filename, icd10_codes=[], icd9_codes=[], death_icd10_codes=[], opcs4_codes=[], all_causes_death=False):
        self.pkl_path = pkl_path
        self.output_path = output_path
        self.output_filename = output_filename
        self.icd10_codes = icd10_codes
        self.icd9_codes = icd9_codes
        self.death_icd10_codes = death_icd10_codes
        self.opcs4_codes = opcs4_codes
        self.all_causes_death = all_causes_death

        # Ensure output directory exists
        os.makedirs(self.output_path, exist_ok=True)

    @staticmethod
    def create_from_args():
        parser = argparse.ArgumentParser(description="Process and analyze medical event data.")
        parser.add_argument('--pkl_path', type=Path, required=True, help='Path to the pickle file containing preloaded event data.')
        parser.add_argument('--output_path', type=Path, required=True, help='Directory path for saving the output files.')
        parser.add_argument('--output_filename', type=str, required=True, help='Filename for the output CSV file.')
        parser.add_argument('--icd10_codes', type=str, nargs='+', default=[], help='List of ICD10 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.')
        parser.add_argument('--icd9_codes', type=str, nargs='+', default=[], help='List of ICD9 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.')
        parser.add_argument('--death_icd10_codes', type=str, nargs='+', default=[], help='List of Death-related ICD10 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.')
        parser.add_argument('--opcs4_codes', type=str, nargs='+', default=[], help='List of OPCS4 codes of interest or path to text file containing codes. Space-separated if multiple or a single path to a file.')
        parser.add_argument('--all_causes_death', action='store_true', help='Flag to include all-cause mortality in the search.')
        
        args = parser.parse_args()

        # Function to determine if a path is a file or not
        def is_file_path(p):
            return Path(p).is_file()

        # Helper function to process codes input
        def process_codes_input(codes_input):
            # If the input is a single item and it's a file path, read the codes from the file
            if len(codes_input) == 1 and is_file_path(codes_input[0]):
                with open(codes_input[0]) as f:
                    return [line.strip() for line in f if line.strip()]
            # Otherwise, treat it as a list of codes
            return codes_input

        # Process codes input
        icd10_codes = process_codes_input(args.icd10_codes)
        if icd10_codes:
            print(f'ICD10 codes: {icd10_codes}')
            print('Number of ICD10 codes:', len(icd10_codes))
        icd9_codes = process_codes_input(args.icd9_codes)
        if icd9_codes:
            print(f'ICD9 codes: {icd9_codes}')  
            print('Number of ICD9 codes:', len(icd9_codes))
        death_icd10_codes = process_codes_input(args.death_icd10_codes)
        if death_icd10_codes:
            print(f'Death-related ICD10 codes: {death_icd10_codes}')
            print('Number of death-related ICD10 codes:', len(death_icd10_codes))
        opcs4_codes = process_codes_input(args.opcs4_codes)
        if opcs4_codes:
            print(f'OPCS4 codes: {opcs4_codes}')
            print('Number of OPCS4 codes:', len(opcs4_codes))

        return Config(
            pkl_path=args.pkl_path,
            output_path=args.output_path,
            output_filename=args.output_filename,
            icd10_codes=icd10_codes,
            icd9_codes=icd9_codes,
            death_icd10_codes=death_icd10_codes,
            opcs4_codes=opcs4_codes,
            all_causes_death=args.all_causes_death
        )

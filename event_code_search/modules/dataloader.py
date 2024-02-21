import os
import pandas as pd
import pyreadr
import pickle as pkl
from natsort import natsorted

class DataLoader:
    def __init__(self, dat_path):
        self.dat_path = dat_path
        self.dat = None
        self.headers = None
        self.event_data = None

    def load_data(self):
        print('Reading in outcome data...')
        self.dat = pd.read_csv(self.dat_path, low_memory=False)
        self.headers = pd.DataFrame({"UDI": self.dat.columns})
        print('Outcome data read in.')

    def load_event_data(self, pkl_path):
        print('Reading in event data...')
        with open(pkl_path, 'rb') as f:
            self.event_data = pkl.load(f)
        print('Event data read in.')

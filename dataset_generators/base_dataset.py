import pandas as pd

BASE_DATASET_NAME = "Athletes + PIB Dataset"
BASE_DATASET_PATH = r".\res\athlete_events_with_pib.csv"

class BaseDataset:
    @staticmethod
    def get_name():
        return BASE_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(BASE_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        pass
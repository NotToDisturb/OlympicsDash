import pandas as pd

from dataset_generators.medals_dataset import MedalsDataset

MEDALS_COUNTRY_DATASET_NAME = "Medals"
MEDALS_COUNTRY_DATASET_PATH = r".\res\medals_country_dataset.csv"

class MedalsCountryDataset:
    @staticmethod
    def get_name():
        return MEDALS_COUNTRY_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(MEDALS_COUNTRY_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        df = MedalsDataset.load_data()
        group_keys = ["Year", "NOC", "Gold", "Silver", "Bronze"]
        medals_df = df[group_keys].groupby(group_keys[:2]).sum().reset_index()
        medals_df.to_csv(MEDALS_COUNTRY_DATASET_PATH, index=False)
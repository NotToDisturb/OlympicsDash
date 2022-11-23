import pandas as pd

from dataset_generators.base_dataset import BaseDataset

GENRE_DATASET_NAME = "Gender Dataset"
GENRE_DATASET_PATH = r".\res\gender_dataset.csv"

class GenderDataset:
    @staticmethod
    def get_name():
        return GENRE_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(GENRE_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        df = BaseDataset.load_data()
        df["Women"] = df["Sex"].apply(lambda row: 1 if row == "F" else 0)
        df["Men"] = df["Sex"].apply(lambda row: 1 if row == "M" else 0)
        gender_df = df[["Year", "NOC", "Women", "Men"]].groupby(["Year", "NOC"]).sum().reset_index()
        gender_df.to_csv(GENRE_DATASET_PATH, index=False)
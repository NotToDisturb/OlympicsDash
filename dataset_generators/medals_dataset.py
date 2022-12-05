import pandas as pd

from dataset_generators.base_dataset import BaseDataset

MEDALS_DATASET_NAME = "Medals"
MEDALS_DATASET_PATH = r".\res\medals_dataset.csv"

class MedalsDataset:
    @staticmethod
    def get_name():
        return MEDALS_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(MEDALS_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        df = BaseDataset.load_data()
        # Add a column containing with a binary value for the medals won
        df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)       # Won a gold medal
        df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)   # Won a silver medal
        df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)   # Won a bronze medal
        df["Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]                     # Won any medal
        medals_df = df[["Year", "NOC", "Team", "Continent", "Sport", "Gold", "Silver", "Bronze", "Medals", "PIB"]]
        medals_df.to_csv(MEDALS_DATASET_PATH, index=False)
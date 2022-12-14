import pandas as pd
import numpy as np

from dataset_generators.base_dataset import BaseDataset

PIB_DATASET_NAME = "PIB/MEDALS PER YEAR"
PIB_DATASET_PATH = r".\res\pib_dataset.csv"

class PIBDataset:
    @staticmethod
    def get_name():
        return PIB_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(PIB_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        df = BaseDataset.load_data()
        df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)       # Won a gold medal
        df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)   # Won a silver medal
        df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)   # Won a bronze medal
        df["Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]                     # Won any medal
        group_keys = ["Year", "NOC", "Continent", "PIB"]
        pib_df = df[["Year", "NOC", "Continent", "Medals", "PIB"]].groupby(group_keys).sum().reset_index()
        pib_df["PIB/MEDALS"] = pib_df['PIB'].div(pib_df['Medals']).replace(np.inf, 0)
        pib_df.to_csv(PIB_DATASET_PATH, index=False)
       
    
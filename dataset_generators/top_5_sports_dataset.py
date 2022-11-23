import pandas as pd

from dataset_generators.medals_dataset import MedalsDataset

TOP_5_SPORTS_DATASET_NAME = "Top 5 Sports Dataset"
TOP_5_SPORTS_DATASET_PATH = r".\res\top_5_sports_dataset.csv"

class Top5SportsDataset:
    @staticmethod
    def get_name():
        return TOP_5_SPORTS_DATASET_NAME

    @staticmethod
    def load_data():
        return pd.read_csv(TOP_5_SPORTS_DATASET_PATH, encoding="latin1")

    @staticmethod
    def build_dataset():
        df = MedalsDataset.load_data()
        df_top = df[["Year", "NOC", "Sport", "Medals"]].groupby(["Year", "NOC", "Sport"]).sum().reset_index()
        years = df_top["Year"].unique()
        countries = df_top["NOC"].unique()
        cols = ["Year", "NOC", "Sport 1", "Medals 1", "Sport 2", "Medals 2", "Sport 3", 
            "Medals 3", "Sport 4", "Medals 4", "Sport 5", "Medals 5"]
        output_df = pd.DataFrame([], columns=cols)
        for year in years:
            for country in countries:
                try:
                    aux = df_top.loc[(df_top["Year"]==year) & (df_top["NOC"]==country)].nlargest(5, "Medals")
                except:
                    continue
                if aux["Medals"].sum() == 0:
                    continue
                data = [year, country]
                for i in range(5):
                    try:
                        med = aux.iloc[i, 3]
                        if med != 0:
                            data.append(aux.iloc[i, 2])
                            data.append(med)
                        else:
                            data.append("")
                            data.append("")
                    except:
                        data.append("")
                        data.append("")
                output_df = pd.concat([output_df, pd.DataFrame([data], columns=cols)], ignore_index=True)
        output_df.to_csv(TOP_5_SPORTS_DATASET_PATH, index=False)
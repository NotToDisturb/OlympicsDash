import pandas as pd
import plotly.express as px


DATASET = r".\res\athlete_events_with_pib.csv"


def load_data():
    df = pd.read_csv(DATASET, encoding="latin1")
    df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)
    df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)
    df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)
    df["Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]
    return df


def get_medal_dataframe(df, medal_type):
    group_keys = ["Year", "NOC", "Team", "Continent"]
    df_medal = df[["Year", "NOC", "Team", "Continent", medal_type]].groupby(group_keys).sum().reset_index()
    return df_medal


def build_medals_figure(df_medals, medal_type):
    fig = px.scatter_geo(df_medals, locations="NOC", color="Continent",
                         hover_name="Team", size=medal_type,
                         animation_frame="Year",
                         projection="natural earth")
    return fig

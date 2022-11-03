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


def main():
    df = load_data()
    group_keys = ["Year", "NOC", "Team", "Continent"]
    #df_gold = df[["Year", "NOC", "Team", "Continent", "Gold"]].groupby(group_keys).sum().reset_index()
    #df_silver = df[["Year", "NOC", "Team", "Continent", "Silver"]].groupby(group_keys).sum().reset_index()
    #df_bronze = df[["Year", "NOC", "Team", "Continent", "Bronze"]].groupby(group_keys).sum().reset_index()
    df_medals = df[["Year", "NOC", "Team", "Continent", "Medals"]].groupby(group_keys).sum().reset_index()

    continent_medals = df_medals[df_medals["Continent"].str.contains("Africa")]
    year_medals = continent_medals[continent_medals["Medals"] != 0]
    print(year_medals)

    fig = px.scatter_geo(df_medals, locations="NOC", color="Continent",
                         hover_name="Team", size="Medals",
                         animation_frame="Year",
                         projection="natural earth")
    fig.show()


if __name__ == "__main__":
    main()

import pandas as pd
import plotly.express as px

DATASET = r".\res\athlete_events_with_pib.csv"


def load_data():
    df = pd.read_csv(DATASET)
    df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)
    df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)
    df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)
    return df


def main():
    df = load_data()
    df = df.groupby(by="NOC").sum().reset_index()

    print(df)

    fig = px.scatter_geo(df, locations="NOC", color="NOC",
                         hover_name="NOC", size="Gold",
                         animation_frame="Year",
                         projection="natural earth")
    fig.show()


if __name__ == "__main__":
    main()

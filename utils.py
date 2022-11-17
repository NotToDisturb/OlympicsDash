import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import dcc

# Relative path to dataset
DATASET = r".\res\athlete_events_with_pib.csv"


# Load the dataset
def load_data():
    df = pd.read_csv(DATASET, encoding="latin1")
    # Add a column containing with a binary value for the medals won
    df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)       # Won a gold medal
    df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)   # Won a silver medal
    df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)   # Won a bronze medal
    df["Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]                     # Won any medal
    return df


# Get the yearly sum of medals of a type
def get_medal_dataframe(df, medal_type):
    group_keys = ["Year", "NOC", "Team", "Continent"]
    df_medal = df[["Year", "NOC", "Team", "Continent", medal_type]].groupby(group_keys).sum().reset_index()
    return df_medal


# Build a slider object to select which year to display in the dashboard map
# It sets up the minimum and maximum year, all the acceptable years and the starting year
def build_year_slider(df):
    years = df["Year"].unique()
    slider = dcc.Slider(
        id='years-slider', min=int(min(years)), max=int(max(years)), 
        step=None, value=int(max(years)), included=False,
        marks=dict(sorted({int(year): str(year) for year in years}.items()))
    )
    return slider

# Build the dictionary of yearly medals for a medal type
def build_medals_figures(df_medals, medal_type):
    years = df_medals["Year"].unique()
    fig_years = {}
    for year in years:
        # Select medals of a given year
        df_medals_year = df_medals[df_medals["Year"] == year]
        # Create scatter plot using:
        # - Country code as locator
        # - Continent as the color
        # - Country as the hover text
        # - Medal count as the size
        # - "natural earth" as the map type
        fig_year = px.scatter_geo(df_medals_year, locations="NOC", color="Continent",
                         hover_name="Team", size=medal_type,
                         projection="natural earth")
        fig_years[year] = fig_year
    return fig_years


def create_data_genres():
    df = pd.read_csv(DATASET, encoding="latin1")
    df["Women"] = df["Sex"].apply(lambda row: 1 if row == "F" else 0)
    df["Men"] = df["Sex"].apply(lambda row: 1 if row == "M" else 0)
    df_genre = df[["Year", "NOC", "Women", "Men"]].groupby(["Year", "NOC"]).sum().reset_index()
    df_genre.to_csv("res/genre_data.csv", index=False)
    return df_genre

def create_data_medals():
    df = load_data()
    df_medal = df[["Year", "NOC", "Gold", "Silver", "Bronze"]].groupby(["Year", "NOC"]).sum().reset_index()
    df_medal.to_csv("res/medallero_graph.csv", index=False)

def create_data_top5_sports():
    df = load_data()
    df_top = df[["Year", "NOC", "Sport", "Medals"]].groupby(["Year", "NOC", "Sport"]).sum().reset_index()
    years = df_top["Year"].unique()
    countries = df_top["NOC"].unique()
    cols = ["Year", "NOC", "Sport 1", "Medals 1", "Sport 2", "Medals 2", "Sport 3", 
        "Medals 3", "Sport 4", "Medals 4", "Sport 5", "Medals 5"]
    output = pd.DataFrame([], columns=cols)
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
            output = pd.concat([output, pd.DataFrame([data], columns=cols)], ignore_index=True)
    output.to_csv("res/top5_sports.csv", index=False)

# Creates the genre graphs and returns it
def create_genre_graph(year, noc):
    df = pd.read_csv("res/genre_data.csv")
    # Auxiliar information
    colors = ["#FE90C0","#9ACDDD"]
    labels = ['Women','Men']
    values = df.loc[(df["Year"]==year) & (df["NOC"]==noc)].iloc[:,-2:].values[0].tolist()
    perc = round(max(values)/(max(values)+min(values))*100,1)
    texto = f"{perc}%<br>{labels[values.index(max(values))]}"
    title_info = go.pie.Title(text=texto, font={"size":18})
    # Graph
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, title=title_info)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(paper_bgcolor='#DDD9D9', width=400, height=400)
    return fig

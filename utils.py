import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import dcc

GRAPH_HEIGHT = 200
GRAPH_WIDTH = 300

# Get the yearly sum of medals of a type
def get_medal_dataframe(df, medal_type):
    group_keys = ["Year", "NOC", "Team", "Continent"]
    df_medal = df[group_keys + [medal_type]].groupby(group_keys).sum().reset_index()
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
def build_medals_figures(medals_df, medal_type):
    years = medals_df["Year"].unique()
    fig_years = {}
    for year in years:
        # Select medals of a given year
        df_medals_year = medals_df[medals_df["Year"] == year]
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


# Creates the genre graphs and returns it
def create_genre_graph(gender_df, year, noc):
    """ Creates a participations per genre graph. """
    # Auxiliar information
    colors = ["#FE90C0","#9ACDDD"]
    labels = ['Women','Men']
    # We obtain the number of participants per gender given a year and a country from the dataframe.
    values = gender_df.loc[(gender_df["Year"]==year) & (gender_df["NOC"]==noc)].iloc[:,-2:].values[0].tolist()
    # Percentaje to show it in the title.
    perc = round(max(values)/(max(values)+min(values))*100,1)
    # Title information.
    texto = f"{perc}%<br>{labels[values.index(max(values))]}"
    title_info = go.pie.Title(text=texto, font={"size":13})
    # Pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, title=title_info)])
    # Styling additions.
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(paper_bgcolor='#DDD9D9', width=GRAPH_WIDTH, height=GRAPH_HEIGHT, margin=dict(l=30,r=30,b=5,t=5))
    return fig

def create_top5_graph(top5_df, year, noc):
    """ Creates a top 5 sports per country in a year graph. """
    # We get the 5 best sports and medals for the country and year given using the dataframe.
    values = top5_df.loc[(top5_df["Year"]==year) & (top5_df["NOC"]==noc)].iloc[:,2:].values[0].tolist()
    colors = ["#80A3AE", "#9ACDDD", "#F29F9F", "#B6DB94", "#F9F4A6"]
    # Inverse range from 5 to 1.
    y = [i for i in range(5,0,-1)]
    # Number of medals per sport.
    x = [values[9], values[7], values[5], values[3], values[1]]
    # Name of the sports.
    deportes = [values[8], values[6], values[4], values[2], values[0]]
    # Bar chart.
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker=dict(color=colors, line=dict(color='#FFFFFF', width=2)),orientation='h')])
    # Styling additions.
    fig.update_traces(text=deportes, hovertemplate="Position %{text}<br>%{x} medals")
    fig.update_layout(paper_bgcolor='#DDD9D9', plot_bgcolor='rgba(0,0,0,0)', width=GRAPH_WIDTH, height=GRAPH_HEIGHT, 
        xaxis = dict(side ="top"), margin=dict(l=5,r=10,b=5,t=5, pad=5))
    return fig

def create_medals_country_graph(med_df, year, noc):
    """ Creates a medals per country in a year graph. """
    # Auxiliar information
    colors = ["#DFD082","#7D8398","#B98A67"]
    labels = ['Gold','Silver', 'Bronze']
    # We get the number of gold, silver and bronze medals from the dataframe.
    values = med_df.loc[(med_df["Year"]==year) & (med_df["NOC"]==noc)].iloc[:,-3:].values[0].tolist()
    # Pie chart.
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)])
    # Styling additions.
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=15,
                  marker=dict(colors=colors, line=dict(color='#FFFFFF', width=2)))
    fig.update_layout(paper_bgcolor='#DDD9D9', width=GRAPH_WIDTH, height=GRAPH_HEIGHT, margin=dict(l=30,r=30,b=5,t=5))
    return fig

def create_pib_graph(pib_df, year, noc):
    """ Creates a PIB per country graph """
    # Gets all the values for a given country in the PIB dataframe.
    values = pib_df.loc[(pib_df["NOC"]==noc)]
    # Insert the different categories into arrays.
    years = values["Year"].values
    medals = values["Medals"].values
    pibs = values["PIB"].values
    # We need to remark the color of the year we are visualizing.
    colors = ['#7D8398'] * len(years)
    # If we don't have data for that year we cannot create the graph.
    try:
        colors[list(years).index(year)] = "#01FFF4"
    except:
        return None
    # We need two graphs, so we make a template.
    fig = make_subplots(rows=1, cols=1,
        specs=[[{"secondary_y": True}]])
    # Bar chart.
    fig.add_trace(go.Bar(x=years, y=medals, yaxis="y1", marker=dict(color=colors), name="medals", 
        hovertemplate="Year: %{x}.<br>Medals: %{y}"), row=1, col=1, secondary_y=False)
    # Line chart.
    fig.add_trace(go.Scatter(x=years, y=pibs, yaxis="y2", mode="lines", marker=dict(color="#FE0000"), name="pib", hovertemplate="Year: %{x}.<br>PIB: %{y}"), 
        row=1, col=1, secondary_y=True)
    # Styling additions.
    fig.update_layout(paper_bgcolor='#DDD9D9', plot_bgcolor='rgba(0,0,0,0)', width=GRAPH_WIDTH, height=GRAPH_HEIGHT, 
        margin=dict(l=30,r=30,b=5,t=5), legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig
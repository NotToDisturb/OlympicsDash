import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

app = Dash(__name__)
DATASET = r".\res\athlete_events_with_pib.csv"


def load_data():
    df = pd.read_csv(DATASET, encoding="latin1")
    df["Gold"] = df["Medal"].apply(lambda row: 1 if row == "Gold" else 0)
    df["Silver"] = df["Medal"].apply(lambda row: 1 if row == "Silver" else 0)
    df["Bronze"] = df["Medal"].apply(lambda row: 1 if row == "Bronze" else 0)
    df["Medals"] = df["Gold"] + df["Silver"] + df["Bronze"]
    return df


def build_medal_dataframe(df, medal_str):
    df = load_data()
    group_keys = ["Year", "NOC", "Team", "Continent"]
    df_medal = df[["Year", "NOC", "Team", "Continent", medal_str]].groupby(group_keys).sum().reset_index()

    return df_medal


def build_medals_plot(df_medals, size_str):
    fig = px.scatter_geo(df_medals, locations="NOC", color="Continent",
                         hover_name="Team", size=size_str,
                         animation_frame="Year",
                         projection="natural earth")
    return fig


def main():
    df = load_data()

    df_medals = build_medal_dataframe(df, "Medals")

    fig_medals = build_medals_plot(df_medals, "Medals")

    app.title = "OlympicsDash"
    app.layout = html.Div(children=[
        html.H1(children="OlympicsDash"),

        html.Div(children="The place to look for all things Olympics data."),

        html.Div([
            html.Button(id="gold-medals-button", n_clicks_timestamp=0, children="Oros"),
            html.Button(id="silver-medals-button", n_clicks_timestamp=0, children="Platas"),
            html.Button(id="bronze-medals-button", n_clicks_timestamp=0, children="Bronzes"),
            html.Button(id="all-medals-button", n_clicks_timestamp=0, children="Total")
        ]),

        html.H2(id="title-text", children=""),
        dcc.Graph(
            id='medals-graph',
            figure=fig_medals
        ),
        html.Div(id="latest-country-text", children="")
    ])


@app.callback(
    Output('gold-medals-button', 'disabled'),
    Output('silver-medals-button', 'disabled'),
    Output('bronze-medals-button', 'disabled'),
    Output('all-medals-button', 'disabled'),
    Input('gold-medals-button', 'n_clicks_timestamp'),
    Input('silver-medals-button', 'n_clicks_timestamp'),
    Input('bronze-medals-button', 'n_clicks_timestamp'),
    Input('all-medals-button', 'n_clicks_timestamp')
)
def update_buttons_click(gold_click, silver_click, bronze_click, all_click):
    clicks_buttons = {
        "gold-medal-button": gold_click,
        "silver-medal-button": silver_click,
        "bronze-medal-button": bronze_click,
        "all-medal-button": all_click
    }
    clicked_button = max(clicks_buttons, key=lambda c: clicks_buttons[c])
    disabled = []
    for button in clicks_buttons.keys():
        disabled.append(button == clicked_button)
    return tuple(disabled)


@app.callback(
    Output('title-text', 'children'),
    Output('medals-graph', 'figure'),
    Input('gold-medals-button', 'disabled'),
    Input('silver-medals-button', 'disabled'),
    Input('bronze-medals-button', 'disabled'),
    Input('all-medals-button', 'disabled'),
)
def update_graph_click(gold_disabled, silver_disabled, bronze_disabled, all_disabled):
    disabled_buttons = {
        "gold-medal-button": gold_disabled,
        "silver-medal-button": silver_disabled,
        "bronze-medal-button": bronze_disabled,
        "all-medal-button": all_disabled
    }
    medal_str = {
        "gold-medal-button": "Gold",
        "silver-medal-button": "Silver",
        "bronze-medal-button": "Bronze",
        "all-medal-button": "Medals"
    }

    disabled_str = ""
    for button, disabled in disabled_buttons.items():
        if disabled:
            disabled_str = medal_str[button]
            break

    df = load_data()
    df_processed = build_medal_dataframe(df, disabled_str)
    fig_processed = build_medals_plot(df_processed, disabled_str)
    return disabled_str, fig_processed


@app.callback(
    Output('latest-country-text', 'children'),
    Input('medals-graph', 'clickData')
)
def print_country(click_data):
    print(click_data)
    return str(click_data)


if __name__ == "__main__":
    main()
    app.run_server(debug=True)

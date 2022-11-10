from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

from utils import load_data, get_medal_dataframe, build_medals_figures, build_year_slider

# external_stylesheets = [
#     './styles/style.css'
# ]
# external_stylesheets=external_stylesheets

app = Dash(__name__ )
df = load_data()
medal_maps = {
    "gold-medal": {
        "name": "Oro",
        "type": "Gold",
        "data": get_medal_dataframe(df, "Gold"),
        "figures": None
    },
    "silver-medal": {
        "name": "Plata",
        "type": "Silver",
        "data": get_medal_dataframe(df, "Silver"),
        "figures": None
    },
    "bronze-medal": {
        "name": "Bronce",
        "type": "Bronze",
        "data": get_medal_dataframe(df, "Bronze"),
        "figures": None
    },
    "all-medals": {
        "name": "Total",
        "type": "Medals",
        "data": get_medal_dataframe(df, "Medals"),
        "figures": None
    }
}
def main():
    init_figures()
    years = df["Year"].unique()

    app.title = "OlympicsDash"
    app.layout = html.Div(
        children=[
            html.H1(children="OlympicsDash"),

            html.Div(children="The place to look for all things Olympics data."),

            html.Div([
                html.Button(id="gold-medals-button", n_clicks_timestamp=0, children="Oros"),
                html.Button(id="silver-medals-button", n_clicks_timestamp=0, children="Platas"),
                html.Button(id="bronze-medals-button", n_clicks_timestamp=0, children="Bronzes"),
                html.Button(id="all-medals-button", n_clicks_timestamp=0, children="Total")
            ]),

            html.H2(id="title-text", children=medal_maps["gold-medal"]["name"]),
            dcc.Graph(
                id='medals-graph',
                figure=medal_maps["gold-medal"]["figures"][1960]
            ),
            build_year_slider(df),
            html.Div(id="selected-country-text", children="ESP"),
            html.Div(id="selected-year-text", children="2016")
        ]
    )


def init_figures():
    for medal_map in medal_maps.values():
        medal_map["figures"] = build_medals_figures(medal_map["data"], medal_map["type"])


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


button_to_map = {
    "gold-medal-button": "gold-medal",
    "silver-medal-button": "silver-medal",
    "bronze-medal-button": "bronze-medal",
    "all-medal-button": "all-medals"
}

@app.callback(
    Output('title-text', 'children'),
    Output('medals-graph', 'figure'),
    Input('years-slider', "drag_value"),
    Input('gold-medals-button', 'disabled'),
    Input('silver-medals-button', 'disabled'),
    Input('bronze-medals-button', 'disabled'),
    Input('all-medals-button', 'disabled')
)
def update_graph(select_year, gold_disabled, silver_disabled, bronze_disabled, all_disabled):
    disabled_buttons = {
        "gold-medal-button": gold_disabled,
        "silver-medal-button": silver_disabled,
        "bronze-medal-button": bronze_disabled,
        "all-medal-button": all_disabled
    }
    disabled_map = None
    for button, disabled in disabled_buttons.items():
        if disabled:
            disabled_map = medal_maps[button_to_map[button]]
            break

    return disabled_map["name"], disabled_map["figures"][select_year]


@app.callback(
    Output('selected-country-text', 'children'),
    Input('medals-graph', 'clickData'),
    Input('selected-country-text', 'children')
)
def print_country(select_country, selected_cc):
    return selected_cc if not select_country else select_country["points"][0]["location"]


@app.callback(
    Output('selected-year-text', 'children'),
    Input('years-slider', 'drag_value'),
    Input('selected-year-text', 'children')
)
def print_year(select_year, selected_year):
    return selected_year if not selected_year else select_year


if __name__ == "__main__":
    main()
    app.run_server(debug=True)

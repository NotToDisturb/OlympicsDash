from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

from dataset_generators.medals_dataset import MedalsDataset
from dataset_generators.medals_country_dataset import MedalsCountryDataset
from dataset_generators.gender_dataset import GenderDataset
from dataset_generators.top_5_sports_dataset import Top5SportsDataset
from dataset_generators.pib_dataset import PIBDataset
from utils import get_medal_dataframe, build_medals_figures, build_year_slider, create_genre_graph, create_top5_graph, create_medals_country_graph

# external_stylesheets = [
#     './styles/style.css'
# ]
# external_stylesheets=external_stylesheets

app = Dash(__name__ )
MedalsCountryDataset.build_dataset()
medals_c_df = MedalsCountryDataset.load_data()
medals_df = MedalsDataset.load_data()
gender_df = GenderDataset.load_data()
top5_df = Top5SportsDataset.load_data()
pib_df = PIBDataset.load_data()

# Dictionary containing medal data for the maps
# The medal data is loaded on creation but figures are created separately in order to reuse the loaded data
# For each medal type the fields are:
# - name: the name to be shown on the dashboard
# - type: internal name of the data
# - data: the data from the medal type
# - figures: yearly representations of the medal data (set in init_figures())
medal_maps = {
    "gold-medal": {
        "name": "Oro",
        "type": "Gold",
        "data": get_medal_dataframe(medals_df, "Gold"),
        "figures": None
    },
    "silver-medal": {
        "name": "Plata",
        "type": "Silver",
        "data": get_medal_dataframe(medals_df, "Silver"),
        "figures": None
    },
    "bronze-medal": {
        "name": "Bronce",
        "type": "Bronze",
        "data": get_medal_dataframe(medals_df, "Bronze"),
        "figures": None
    },
    "all-medals": {
        "name": "Total",
        "type": "Medals",
        "data": get_medal_dataframe(medals_df, "Medals"),
        "figures": None
    }
}
# Init medal figures
def init_figures():
    for medal_map in medal_maps.values():
        medal_map["figures"] = build_medals_figures(medal_map["data"], medal_map["type"])


def main():
    init_figures()
    #years = df["Year"].unique()

    app.title = "OlympicsDash"
    app.layout = html.Div(
        children=[
            html.H1(children="OlympicsDash"),
            html.Div(children="The place to look for all things Olympics data."),

            # Selected country and year selected
            
            html.Div([
                # Buttons to select medal map
                html.Div([
                    html.Button(id="gold-medals-button", n_clicks_timestamp=0, children="Oros"),
                    html.Button(id="silver-medals-button", n_clicks_timestamp=0, children="Platas"),
                    html.Button(id="bronze-medals-button", n_clicks_timestamp=0, children="Bronzes"),
                    html.Button(id="all-medals-button", n_clicks_timestamp=0, children="Total")
                ]),

                # Title, map and slider
                html.H2(id="title-text", children=medal_maps["gold-medal"]["name"]),
                dcc.Graph(
                    id='medals-graph',
                    figure=medal_maps["gold-medal"]["figures"][1960]
                ),
                build_year_slider(medals_df)
            ]),
            html.Div(id="country_data", children=[
                html.Div(className="cd_class", children=[
                    html.Div(id="selected-country-text", className='selector', children="ESP"),
                    html.Div(id="selected-year-text", className='selector', children="2016")
                ]),
                html.Div(id="graph_container", className="cd_class", 
                    children=[
                    html.Div(id="graph_piv_div", className='grafico_div'),
                    html.Div(id="graph_genre_div",  className='grafico_div',
                    children=[
                        html.H2(children=GenderDataset.get_name()),
                        dcc.Graph(
                            id='graph_genre',
                            className='grafico',
                            figure=create_genre_graph(gender_df, 2016, "ESP")
                        )
                    ]),
                    html.Div(id="graph_top_sports_div", className='grafico_div',
                    children=[
                        html.H2(children=Top5SportsDataset.get_name()),
                        dcc.Graph(
                            id='graph_top5',
                            className='grafico',
                            figure=create_top5_graph(top5_df, 2016, "ESP")
                        )]),
                    html.Div(id="graph_medals_country_div", className='grafico_div',
                    children=[
                        html.H2(children=MedalsCountryDataset.get_name()),
                        dcc.Graph(
                            id='graph_medals_country',
                            className='grafico',
                            figure=create_medals_country_graph(medals_c_df, 2016, "ESP")
                        )
                    ])
                ])
            ])
        ]
    )


# When a map selection button is clicked, the clicked button is disabled and all others enabled
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
    # Map input times to button ids
    clicks_buttons = {
        "gold-medal-button": gold_click,
        "silver-medal-button": silver_click,
        "bronze-medal-button": bronze_click,
        "all-medal-button": all_click
    }
    # Get the key with the highest value (latest click)
    clicked_button = max(clicks_buttons, key=lambda c: clicks_buttons[c])
    # Build list of button states
    disabled = []
    for button in clicks_buttons.keys():
        disabled.append(button == clicked_button)
    return tuple(disabled)


# Dictionary mapping button ids to medal types
button_to_map = {
    "gold-medal-button": "gold-medal",
    "silver-medal-button": "silver-medal",
    "bronze-medal-button": "bronze-medal",
    "all-medal-button": "all-medals"
}
# Update shown figure depending on disabled button and selected country
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
    # Map button states to button ids
    disabled_buttons = {
        "gold-medal-button": gold_disabled,
        "silver-medal-button": silver_disabled,
        "bronze-medal-button": bronze_disabled,
        "all-medal-button": all_disabled
    }
    # Get all selected yearly maps by finding disabled button
    disabled_map = None
    for button, disabled in disabled_buttons.items():
        if disabled:
            disabled_map = medal_maps[button_to_map[button]]
            break
    
    # Return medal name and selected yearly map
    return disabled_map["name"], disabled_map["figures"][select_year]

# Show the selected country
@app.callback(
    Output('selected-country-text', 'children'),
    Input('medals-graph', 'clickData'),
    Input('selected-country-text', 'children')
)
def print_country(select_country, selected_cc):
    return selected_cc if not select_country else select_country["points"][0]["location"]

# Show the selected year
@app.callback(
    Output('selected-year-text', 'children'),
    Input('years-slider', 'drag_value'),
    Input('selected-year-text', 'children')
)
def print_year(select_year, selected_year):
    return selected_year if not select_year else select_year

# Build the genre graph
@app.callback(
    Output('graph_genre', 'figure'),
    Input('selected-year-text', 'children'),
    Input('selected-country-text', 'children')
)
def update_genre(sel_year, sel_country):
    return create_genre_graph(gender_df, int(sel_year), sel_country)

# Build the top 5 sports graph
@app.callback(
    Output('graph_top5', 'figure'),
    Input('selected-year-text', 'children'),
    Input('selected-country-text', 'children')
)
def update_genre(sel_year, sel_country):
    return create_top5_graph(top5_df, int(sel_year), sel_country)

# Build the medals per country graph
@app.callback(
    Output('graph_medals_country', 'figure'),
    Input('selected-year-text', 'children'),
    Input('selected-country-text', 'children')
)
def update_genre(sel_year, sel_country):
    return create_medals_country_graph(medals_c_df, int(sel_year), sel_country)

if __name__ == "__main__":
    main()
    app.run_server(debug=True)

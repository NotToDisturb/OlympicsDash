import pandas as pd
import plotly.express as px

DATASET = r".\res\athlete_events_with_pib.csv"

df = pd.read_csv(DATASET)
df = px.data.gapminder()
fig = px.scatter_geo(df, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",
                     animation_frame="year",
                     projection="natural earth")
fig.show()

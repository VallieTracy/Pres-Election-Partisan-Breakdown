# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json


with urlopen('https://www.sos.state.mn.us/media/2791/mn-precincts.json') as response:
    precincts = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, requests_pathname_prefix = '/precinct/', serve_locally = False)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# Set file path
csvpath = "Resources/2016-precinct-president.csv"

# Read csv and setup the dataframe
prec_df = pd.read_csv(csvpath, encoding="ISO-8859-1")
mn_prec_df = prec_df.loc[prec_df['state'] == 'Minnesota']
mn_prec_df = mn_prec_df[["precinct", "votes"]]
mn_prec_df = mn_prec_df.groupby(mn_prec_df["precinct"], as_index=False).sum()

split_prec = mn_prec_df["precinct"].str.split("|", expand=True)
mn_prec_df["new_prec"] = split_prec[0]
mn_prec_df["new_prec"] = mn_prec_df["new_prec"].str.title()


test_csv = "test_precinct.csv"
test_df = pd.read_csv(test_csv)

fig = px.choropleth_mapbox(test_df, geojson=precincts, locations='new_prec', featureidkey = "properties.Precinct", color='votes',
                        color_continuous_scale="Bluered_r",
                        range_color=(0, 300000),
                        mapbox_style="carto-positron",
                        zoom=5, center = {"lat": 46.7296, "lon": -94.6859},
                        opacity=0.5,
                        labels={'Total Votes':'votes'}
                        )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
app.layout = html.Div(children=[

    dcc.Graph(
        id='precinct-graph',
        figure=fig
    )
])

# prec_df = pd.read_csv(csvpath, encoding="ISO-8859-1")
# mn_prec_df = prec_df.loc[prec_df['state'] == 'Minnesota']
# fig = px.scatter_mapbox(mn_prec_df, lat="county_lat", lon="county_long", hover_name="county_name", hover_data=["state", "precinct"],
#                         color_discrete_sequence=["fuchsia"], zoom=5, height=300)
# fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "source": [
#                 "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
#             ]
#         }
#       ])
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
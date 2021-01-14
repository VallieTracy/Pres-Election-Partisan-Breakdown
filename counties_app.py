# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, requests_pathname_prefix = '/counties/', serve_locally = False)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

countiesDF = pd.read_csv("Resources/countypres_2000-2016.csv")

df2016 = countiesDF[(countiesDF["year"]==2016)]
df2016 = df2016.groupby(['FIPS', 'county'], as_index = False).sum()

fig = px.choropleth_mapbox(df2016, geojson=counties, locations='FIPS', color='totalvotes',
                        color_continuous_scale="Viridis",
                        range_color=(0, 300000),
                        mapbox_style="carto-positron",
                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                        opacity=0.5,
                        labels={'Total Votes':'totalvotes'}
                        )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app.layout = html.Div(children=[
       html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),

    dcc.Graph(
        # id='counties-graph',
        id="mapContainer",
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, requests_pathname_prefix = '/counties/', serve_locally = False)


df2016_reps = pd.read_csv("Resources/usa_counties.csv", dtype = {"FIPS": object, "combined_rank": object})


colorscale = {'104' : 'hsl(240,50%,50%)', '106': 'hsl(300,50%,50%)', '110': 'hsl(0,50%,50%)',
             '204': 'hsl(240,65%,50%)', '206': 'hsl(300,65%,50%)', '210': 'hsl(0,65%,50%)',
             '304': 'hsl(240,80%,50%)', '306': 'hsl(300,80%,50%)', '310': 'hsl(0,80%,50%)',
             '404': 'hsl(240,95%,50%)', '406': 'hsl(300,95%,50%)', '410': 'hsl(0,95%,50%)'
}

legend_names = {'104' : 'Low Pop, Low Rep', '106': 'Low Pop, Med Rep', '110': 'Low Pop, High Rep',
             '204': 'Med Low Pop, Low Rep', '206': 'Med Low Pop, Med Rep', '210': 'Med Low Pop, High Rep',
             '304': 'Med High Pop, Low Rep', '306': 'Med High Pop, Med Rep', '310': 'Med High Pop, High Rep',
             '404': 'High Pop, Low Rep', '406': 'High Pop, Med Rep', '410': 'High Pop, High Rep'
}

#df2016_reps["combined_rank"] = df2016_reps["combined_rank"].astype(str)

# fig = px.choropleth_mapbox(df2016_reps, geojson=counties, locations='FIPS', color='combined_rank',
#                         color_discrete_map = colorscale,
#                         mapbox_style="carto-positron",
#                         zoom=3.25, center = {"lat": 37.0902, "lon": -95.7129},

#                         opacity=1,
#                         hover_name = "county",
#                         labels={'test':444}
#                         )

fig = px.choropleth(df2016_reps, geojson = counties, locations = 'FIPS', color = 'combined_rank', 
                    color_discrete_map = colorscale, scope = 'usa', hover_name = 'county'
                    )

#fig.update_traces(selector = legend_names)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app.layout = html.Div(children=[
       html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),

    dcc.Graph(
        id="mapContainer",
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
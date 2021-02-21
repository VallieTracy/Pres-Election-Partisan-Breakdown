# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from counties_app import colorscale, legend_names

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
stylesheet = [{"href": "/static/css/style.css",
                'rel': 'stylesheet'}]

app = dash.Dash(__name__, requests_pathname_prefix = '/precinct/', serve_locally = False)


prec_df = pd.read_csv("Resources/mn_precincts.csv", dtype =  {"combined_rank": object})
#prec_df["combined_rank"] = prec_df["combined_rank"].astype(str)

# fig = px.choropleth_mapbox(prec_df, geojson=precincts, locations='VTDID', featureidkey = "properties.PrecinctID", color='combined_rank',
#                         color_discrete_map = colorscale,
#                         mapbox_style="carto-positron",
#                         zoom=5, center = {"lat": 46.7296, "lon": -94.6859},
#                         opacity=1,
#                         labels={'Total Votes':'votes'}
                        
#                         )

fig = px.choropleth(prec_df, geojson = precincts, locations = 'VTDID', featureidkey = "properties.PrecinctID", color = 'combined_rank', 
                    color_discrete_map = colorscale, hover_name = 'PCTNAME'
                    )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app.layout = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),

    dcc.Graph(
        id='precinct-graph',

        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
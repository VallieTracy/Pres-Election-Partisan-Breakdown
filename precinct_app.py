# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from counties_app import label_pct, pop_rank, combined_rank, colorscale

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
# external_stylesheets= stylesheet, 

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

csvpath = "Resources/2016_precincts_newVersion.csv"
prec_df = pd.read_csv(csvpath, encoding="ISO-8859-1")

prec_df = prec_df[['VTDID', 'PCTNAME', 'PCTCODE', 'MCDNAME', 'COUNTYNAME', 'COUNTYCODE',
                   'USPRSR', 'USPRSDFL', 'USPRSTOTAL']][:-1]

prec_df = prec_df.rename(columns = {'MCDNAME': 'Munic/Unorg Terr Name',
                                    'USPRSR': 'Trump', 'USPRSDFL': 'Clinton',
                                    'USPRSTOTAL': 'Total Votes'})

prec_df['percent'] = prec_df['Trump'] / prec_df['Total Votes']


prec_df["pct_rank"] = prec_df.apply (lambda row: label_pct(row), axis=1)
prec_df["pop_rank"] = pd.qcut(prec_df["Total Votes"], q=[0, .25, .5, .75, 1],labels =[1,2,3,4] )
prec_df["combined_rank"] = prec_df.apply (lambda row: combined_rank(row), axis=1)
prec_df["combined_rank"] = prec_df["combined_rank"].astype(str)

fig = px.choropleth_mapbox(prec_df, geojson=precincts, locations='VTDID', featureidkey = "properties.PrecinctID", color='combined_rank',
                        color_discrete_map = colorscale,
                        mapbox_style="carto-positron",
                        zoom=4, center = {"lat": 46.7296, "lon": -94.6859},
                        opacity=1,
                        labels={'Total Votes':'votes'}
                        
                        )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
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
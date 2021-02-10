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
#import plotly.figure_factory as ff

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, requests_pathname_prefix = '/counties/', serve_locally = False)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

countiesDF = pd.read_csv("Resources/countypres_2000-2016.csv")

df2016 = countiesDF[(countiesDF["year"] == 2016)]
df2016_reps = df2016[(df2016["party"]) == "republican"]
df2016_reps["percent"] = df2016_reps["candidatevotes"] / df2016["totalvotes"]

df2016_reps = df2016_reps.dropna(subset = ["FIPS"])
df2016_reps["FIPS"] = df2016_reps["FIPS"].astype(np.int64)
df2016_reps["FIPS"] = df2016_reps["FIPS"].astype(str)

i = 0
while i < len(df2016_reps.index):

    if len(df2016_reps.iloc[i,4])<=4:
        df2016_reps.iloc[i,4] = "0" + df2016_reps.iloc[i,4]
        i+=1
    else:
        i+=1

fips = df2016_reps["FIPS"]
values = df2016_reps["percent"]
valuesPop = df2016_reps["totalvotes"]

#endptsPop = list(np.mgrid[min(valuesPop):max(valuesPop):6j])  # Do we need this?

colorscale = { '104' : 'hsl(240,50%,50%)', '106': 'hsl(300,50%,50%)', '110': 'hsl(0,50%,50%)',
             
             '204': 'hsl(240,65%,50%)', '206': 'hsl(300,65%,50%)', '210': 'hsl(0,65%,50%)',
              
             '304': 'hsl(240,80%,50%)', '306': 'hsl(300,80%,50%)', '310': 'hsl(0,80%,50%)',

              '404': 'hsl(240,95%,50%)', '406': 'hsl(300,95%,50%)', '410': 'hsl(0,95%,50%)'
}


# instead of doing all this in here, and even the trimming the dataframe down to reps
# and year 2016, should we do that all in JN and then export to csv, and then this file
# uses that cleaned up CSV, to save processing time on this?
def label_pct(row):
    if row["percent"] <= .40:
        return 4

    if row["percent"] <= .60:
        return 6

    return 10

def pop_rank(row):
    return pd.qcut(row,5, retbins = True)

def combined_rank(row):
    return row["pop_rank"]*100+row["pct_rank"]

df2016_reps["pct_rank"] = df2016_reps.apply (lambda row: label_pct(row), axis=1)
df2016_reps["pop_rank"] = pd.qcut(df2016_reps["totalvotes"], q=[0, .25, .5, .75, 1],labels =[1,2,3,4] )
df2016_reps["combined_rank"] = df2016_reps.apply (lambda row: combined_rank(row), axis=1)

df2016_reps["combined_rank"] = df2016_reps["combined_rank"].astype(str)

fig = px.choropleth_mapbox(df2016_reps, geojson=counties, locations='FIPS', color='combined_rank',
                        color_discrete_map = colorscale,
                        mapbox_style="carto-positron",
                        zoom=3.25, center = {"lat": 37.0902, "lon": -95.7129},

                        opacity=1,
                        #labels={'totalvotes':'Total Votes'}
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
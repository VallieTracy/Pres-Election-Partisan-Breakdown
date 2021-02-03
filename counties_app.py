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


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

countiesDF = pd.read_csv("Resources/countypres_2000-2016.csv")


df2016 = countiesDF[(countiesDF["year"]==2016)]

df2016_reps = df2016[df2016.party == "republican"]

df2016_reps['percent'] = df2016_reps['candidatevotes'] / df2016_reps['totalvotes']


fips = df2016_reps["FIPS"]
values = df2016_reps["percent"]
valuesPop = df2016_reps["totalvotes"]


colorscale = [ 'hsl(240,50%,50%)', 'hsl(300,50%,50%)','hsl(0,50%,50%)',\
             
             'hsl(240,65%,50%)', 'hsl(300,65%,50%)','hsl(0,65%,50%)',\
              
             'hsl(240,80%,50%)', 'hsl(300,80%,50%)','hsl(0,80%,50%)',\

              
              'hsl(240,95%,50%)', 'hsl(300,95%,50%)','hsl(0,95%,50%)'\
             ]

endptsPop = list(np.mgrid[min(valuesPop):max(valuesPop):6j])


def label_pct(row):
    if row["percent"] <= .20:
        return 2
    if row["percent"] <= .40:
        return 4
    if row["percent"] <= .60:
        return 6
    if row["percent"] <= .80:
        return 8
    return 10

def pop_rank(row):
    return pd.qcut(row,5, retbins = True)

def combined_rank(row):
    return row["pop_rank"]*100+row["pct_rank"]

pd.qcut(df2016_reps["totalvotes"], q=5,labels =[1,2,3,4,5], retbins =True)
df2016_reps["pop_rank"] = pd.qcut(df2016_reps["totalvotes"], q=[0, .25, .5, .75, 1],labels =[1,2,3,4] )
df2016_reps['pop_rank'] = df2016_reps['pop_rank'].astype(int)


df2016_reps["pct_rank"]=df2016_reps.apply (lambda row: label_pct(row), axis=1)
#df2016_reps["pop_rank"]= df2016_reps.apply (lambda row: pop_rank(row), axis=1) #Causes a str to int error when I try to run this line
df2016_reps["combined_rank"]= df2016_reps.apply (lambda row: combined_rank(row), axis=1)

#I think color needs to be on the combined rank....
fig = px.choropleth_mapbox(df2016_reps, geojson=counties, locations='FIPS', color='totalvotes',
                        color_continuous_scale=colorscale,
                        #range_color=(0, 300000),
                        mapbox_style="carto-positsron",
                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                        opacity=0.5,
                        labels={'Total Votes': 'totalvotes'}
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

# The below code doesn't not work, so I'm leaving it to reference back to as I embarque
# on testing out the new stuff.

# countiesDF = pd.read_csv("Resources/countypres_2000-2016.csv")

# df2016 = countiesDF[(countiesDF["year"]==2016)]
# df2016 = df2016.groupby(['FIPS', 'county'], as_index = False).sum()

# fig = px.choropleth_mapbox(df2016, geojson=counties, locations='FIPS', color='totalvotes',
#                         color_continuous_scale="Viridis",
#                         range_color=(0, 300000),
#                         mapbox_style="carto-positron",
#                         zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
#                         opacity=0.5,
#                         labels={'Total Votes':'totalvotes'}
#                         )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# app.layout = html.Div(children=[
#        html.Link(
#         rel='stylesheet',
#         href='/assets/style.css'
#     ),

#     dcc.Graph(
#         # id='counties-graph',
#         id="mapContainer",
#         figure=fig
#     )
# ])

if __name__ == '__main__':
    app.run_server(debug=True)
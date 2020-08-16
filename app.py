# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from flask import Flask, render_template, jsonify
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json

print(dcc.__version__)

    

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

countiesDF = pd.read_csv("Resources/countypres_2000-2016.csv")
#testDict = testDF.to_dict(orient = "index")

df2016 = countiesDF[(countiesDF["year"]==2016)]
df2016 = df2016.groupby(df2016["FIPS"], as_index = False).sum()


fig = px.choropleth_mapbox(df2016, geojson=counties, locations='FIPS', color='totalvotes',
                        color_continuous_scale="Viridis",
                        range_color=(0, 250000),
                        mapbox_style="carto-positron",
                        zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                        opacity=0.5,
                        labels={'Total Votes':'totalvotes', "State": 'states', "County": "county"}
                        )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)




# from flask import Flask, render_template, jsonify
# import numpy as np
# import pandas as pd

# app = Flask(__name__)

# testDB = pd.read_csv("Resources/1976-2016-president.csv")
# testDict = testDB.to_dict(orient = "index")


# @app.route("/")
# def index():
    
#     return render_template("index.html")

# @app.route("/test")
# def test():
#     #return testDict[1]["party"]
    
#     i = 0
#     demCount = 0

#     while i <= len(testDict):
#         if (testDict[i]["party"] == "democrat"):
#             demCount = demCount + testDict[i]["candidatevotes"]

#         i += 1


#     return str(demCount)

#     # if testDict[i]["party"] == "democrat":
#     #     demCount = demCount + testDict[i]["candidatevotes"]
#     # return str(demCount)
        


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine
import numpy as np
import pandas as pd

app = Flask(__name__)

testDB = pd.read_csv("Resources/1976-2016-president.csv")
testDict = testDB.to_dict(orient = "index")


@app.route("/")
def index():
    
    return render_template("index.html")

@app.route("/test")
def test():
    #return testDict[1]["party"]
    
    i = 0
    demCount = 0

    while i <= len(testDict):
        if (testDict[i]["party"] == "democrat"):
            demCount = demCount + testDict[i]["candidatevotes"]

        i += 1


    return str(demCount)

    # if testDict[i]["party"] == "democrat":
    #     demCount = demCount + testDict[i]["candidatevotes"]
    # return str(demCount)
        


if __name__ == "__main__":
    app.run(debug=True)
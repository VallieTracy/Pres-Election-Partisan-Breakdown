# Election Breakdown     
#### <i>Looking at the 2016 Presidential Election voting breakdown, based on party-votes and total ballots casts</i>               
Given how politically fraught the U.S. currently feels, we wanted to explore just how partisan the country actually is.  To answer that question, we looked at what the actual vote tallies were, broken down by Republican and Democrat.  It can feel like the country is intensely either-or.  Either you're a Democrat.  Or you're a Republican.  But we hypothesized that the country is overwhelmingly "purple."  With this project, we strove to show that the people of the U.S. are more similar than not by the diversity of the vote tallies.

## Files Included in This Repo:     
<i>We have many files included in this repo which you will not need if you choose to clone it.  So these are the files you'll need to focus on.</i>      
* Assets folder which contains the `style.css`.
* Resources folder containing the various voting data in CSV format, along with shapefiles used for both MN precincts and US counties.
* Templates folder containing the various html pages, of which there are four.
* Flask app `flask_app.py` which gets called in the final `run.py` file
* Two Dash apps (counties_app.py, precinct_app.py) which contain the code to create both the county and MN precinct maps.
* Overall run.py file which calls the above three files.
* WSGI.py file, which is Django's primary deployment platform.


https://public.opendatasoft.com/explore/dataset/us-county-boundaries/table/?refine.stusab=MN

https://docs.github.com/en/github/managing-large-files/versioning-large-files

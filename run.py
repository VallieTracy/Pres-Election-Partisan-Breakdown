from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask_app import flask_app
from counties_app import app as counties_app
from precinct_app import app as precinct_app

application = DispatcherMiddleware(flask_app, {
    '/counties': counties_app.server,
    '/precinct': precinct_app.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)
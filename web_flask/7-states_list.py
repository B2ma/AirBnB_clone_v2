#!/usr/bin/python3
""" This script starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Outputs list of states """
    states = storage.all("State").values()
    states_sorted = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states_sorted)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ closes current session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

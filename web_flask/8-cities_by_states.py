#!/usr/bin/python3
""" This script starts a Flask web application """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ Outputs list of states and associated cities """
    states = storage.all(State)
    states_sorted = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ closes current session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

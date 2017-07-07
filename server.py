from flask import Flask, render_template, request, jsonify
import os
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from trail_finder import get_geocode, get_list_of_trails


app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/local-hikes.json")
def get_local_hikes():
    address = request.args.get("address")
    distance = request.args.get("distance")

    latitude, longitude = get_geocode(address)

    dict_of_trails, dict_of_lat_lng = get_list_of_trails(latitude, longitude, distance)

    if dict_of_trails:
        return jsonify(dict_of_trails)
    else:
        return jsonify()









if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

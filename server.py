from flask import Flask, render_template, request, jsonify
import os
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from trail_finder import get_geocode, get_list_of_trails, get_trail_attributes, get_trail_photos, get_trail_maps

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

    return jsonify(dict_of_trails)


@app.route("/trails/<trail_id>")
def display_trail_info(trail_id):
    """Make api call for trail attributes and display them."""

    trailhead_attributes = get_trail_attributes(trail_id)
    list_of_photos = get_trail_photos(trail_id)
    trail_maps = get_trail_maps(trail_id)

    return render_template("trail_info.html", trailhead_attributes=trailhead_attributes,
                           list_of_photos=list_of_photos, trail_maps=trail_maps)






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

from flask import Flask, render_template, request, jsonify, session
import os
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.cache import SimpleCache
from trail_finder import (get_geocode, get_dict_of_trails, get_trail_attributes,
                          get_trail_photos, get_trail_maps, get_trailhead_info)

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

app.jinja_env.undefined = StrictUndefined

cache = SimpleCache()


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/local-hikes.json")
def get_local_hikes():
    """tbd """

    address = request.args.get("address")
    distance = request.args.get("distance")

    identifier = (address, distance)
    value = cache.get(identifier)
    if value is not None:
        print "##### cached value", value
        return jsonify(value)

    latitude, longitude = get_geocode(address)

    dict_of_trails = get_dict_of_trails(latitude, longitude, distance)

    value = dict_of_trails
    cache.set(identifier, value, timeout=60 * 5)
    print "####### new value", value
    return jsonify(dict_of_trails)


@app.route("/trails/<trail_id>")
def display_trail_info(trail_id):
    """Make api call for trail attributes and display them."""

    all_trail_data = cache.get(trail_id)
    if all_trail_data is not None:
        print "######### cached trail_id value: ", all_trail_data
        return render_template("trail_info.html", list_attributes=all_trail_data[0],
                               list_photos=all_trail_data[1], list_maps=all_trail_data[2],
                               dict_trail_info=all_trail_data[3])

    list_attributes = get_trail_attributes(trail_id)
    list_photos = get_trail_photos(trail_id)
    list_maps = get_trail_maps(trail_id)
    dict_trail_info = get_trailhead_info(trail_id)

    all_trail_data = [list_attributes, list_photos, list_maps, dict_trail_info]

    cache.set(trail_id, all_trail_data, timeout=60*5)
    # cache.set(trail_id_info, dict_trail_info, timeout=60*5)  ### no "trail_id_info"
    print "########## new trail_id value: ", all_trail_data
    return render_template("trail_info.html", list_attributes=all_trail_data[0],
                           list_photos=all_trail_data[1], list_maps=all_trail_data[2],
                           dict_trail_info=all_trail_data[3])


@app.route("/trail/<trail_id>.json")
def get_trail_data(trail_id):
    """ Get data for a specific trail_id and return it to JS via an Ajax call."""

    all_trail_data = cache.get(trail_id)
    if all_trail_data is not None:
        print "##### cached trail_id value json route:", all_trail_data[3]
        return jsonify(all_trail_data[3])
    else:
        print "###########  FAILED LOGIC"





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

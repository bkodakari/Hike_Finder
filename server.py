from flask import (Flask, render_template, request,
                   jsonify, session, redirect, flash)
import os
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.contrib.cache import SimpleCache
from trail_finder import (get_geocode, get_dict_of_trails, get_trail_attributes,
                          get_trail_photos, get_trail_maps, get_trailhead_info)
# from forecast import get_forecast
from model import connect_to_db, db, User, Trail, Favorite, Rating, Photo

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
        return render_template("trail_info.html",
                               list_attributes=all_trail_data[0],
                               list_photos=all_trail_data[1],
                               list_maps=all_trail_data[2],
                               dict_trail_info=all_trail_data[3],
                               trail_id=trail_id)

    list_attributes = get_trail_attributes(trail_id)
    list_photos = get_trail_photos(trail_id)
    list_maps = get_trail_maps(trail_id)
    dict_trail_info = get_trailhead_info(trail_id)

    all_trail_data = [list_attributes,
                      list_photos,
                      list_maps,
                      dict_trail_info]

    cache.set(trail_id, all_trail_data, timeout=60*5)

    print "########## new trail_id value: ", all_trail_data
    return render_template("trail_info.html",
                           list_attributes=all_trail_data[0],
                           list_photos=all_trail_data[1],
                           list_maps=all_trail_data[2],
                           dict_trail_info=all_trail_data[3],
                           trail_id=trail_id)


@app.route("/trail/<trail_id>.json")
def get_trail_data(trail_id):
    """ Get data for a specific trail_id and return it to JS via an Ajax call."""

    print "############ trail_id", trail_id

    all_trail_data = cache.get(trail_id)
    if all_trail_data is not None:
        print "##### cached trail_id value json route:", all_trail_data[3]
        return jsonify(all_trail_data[3])
    else:
        print "###########  FAILED LOGIC"


@app.route("/register", methods=["GET"])
def registration_form():
    """ Show form for user registration. """

    return render_template("registration_form.html")


@app.route('/register', methods=["POST"])
def registration_process():
    """Process registration."""

    f_name = request.form["f_name"]
    l_name = request.form["l_name"]
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(f_name=f_name, l_name=l_name, username=username,
                    email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(username=username).first()
    session["user_id"] = user.user_id

    flash("User %s %s added." % (f_name, l_name))
    return redirect("/")


@app.route('/login', methods=["GET"])
def login_form():
    """ Show login form. """

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = {"user_id": user.user_id,
                          "username": user.username,
                          "f_name": user.f_name,
                          "l_name": user.l_name,
                          "email": user.email}

    flash("Welcome back, %s!" % (user.f_name))
    return redirect("/user/%s" % (user.user_id))


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route('/user/<user_id>')
def display_user_info(user_id):
    """ Take users to their personal information page. """

    user = User.query.get(user_id)
    return render_template("user_page.html", user=user)


@app.route('/ratings.json', methods=['POST'])
def record_ratings():

    trail_id = request.form.get("trailId")
    user_id = session["user_id"]["user_id"]
    rating = request.form.get("rating")
    trail_name = request.form.get("trailName")

    print "trail_id: ", trail_id
    print "user_id: ", user_id
    print "rating: ", rating
    print "trail_name: ", trail_name

    trail = Trail.query.get(trail_id)

    if not trail:
        new_trail = Trail(trail_id=trail_id, trail_name=trail_name)
        db.session.add(new_trail)
        db.session.commit()

    new_rating = Rating(trail_id=trail_id, user_id=user_id, rating=rating)

    db.session.add(new_rating)
    db.session.commit()

    return jsonify(rating)


@app.route('/add-to-favorites.json', methods=['POST'])
def record_favorites():

    trail_id = request.form.get("trailId")
    user_id = session["user_id"]["user_id"]
    trail_name = request.form.get("trailName")
    tag_id = request.form.get("id")

    print "trail_id: ", trail_id
    print "user_id: ", user_id
    print "trail_name: ", trail_name

    trail = Trail.query.get(trail_id)

    if not trail:
        new_trail = Trail(trail_id=trail_id, trail_name=trail_name)
        db.session.add(new_trail)
        db.session.commit()

    new_favorite = Favorite(trail_id=trail_id, user_id=user_id)

    db.session.add(new_favorite)
    db.session.commit()

    response = {'trailName': trail_name, 'id': tag_id}
    return jsonify(response)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

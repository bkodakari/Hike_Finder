""" Models and database functions for HikeFinder. """

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Model definitions

class User(db.Model):
    """ User information. """

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,)
    f_name = db.Column(db.String(20),
                       nullable=False,)
    l_name = db.Column(db.String(20),
                       nullable=False,)
    username = db.Column(db.String(15),
                         nullable=False,
                         unique=True,)
    email = db.Column(db.Text,
                      nullable=False,)
    password = db.Colum(db.String(20),
                        nullable=False,)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User username=%s user_id=%s>" % (self.username, self.user_id)


class Trail(db.Model):
    """ Trail information. """

    __tablename__ = "trails"

    trail_id = db.Column(db.Integer,
                         primary_key=True,)
    trail_name = db.Column(db.text,
                           nullable=False,)

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Trails trail_id=%s trail_name=%s" % (self.trail_id, self.trail_name)


class Favorite(db.Model):
    """ Favorite trail information for users. """

    __tablename__ = "favorites"

    fav_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True,)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    trail_id = db.Column(db.Integer,
                         db.ForeignKey("trails.trail_id"),
                         nullable=False,)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("favorites", order_by=fav_id))

    # Define relationship to trail
    trail = db.relationship("Trail",
                            backref=db.backref("favorites", order_by=fav_id))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Favorites fav_id=%s trail_id=%s" % (self.fav_id, self.trail_id)


class Rating(db.Model):
    """ Rating of a movie by user. """

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True,)
    trail_id = db.Column(db.Integer,
                         db.ForeignKey("trails.trail_id"),
                         nullable=False,)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False,)
    rating = db.Column(db.Integer,
                       nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to trail
    trail = db.relationship("Trail",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Ratings trail_id=%s rating=%s" % (self.trail_id, self.rating)


class Photo(db.Model):
    """ Uploaded user photos. """

    __tablename__ = "photos"

    photo_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True,)
    trail_id = db.Column(db.Integer,
                         db.ForeignKey("trail.trail_id"),
                         nullable=False,)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False,)
    photo = db.Column(db.text,
                      nullable=False)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("photos", order_by=photo_id))

    # Define relationship to trail
    trail = db.relationship("Trail",
                            backref=db.backref("photos", order_by=photo_id))

    def __repr__(self):
        """ Provide helpful representation when printed. """

        return "<Photos photo_id=%s trail_id=%s" % (self.photo_id, self.trail_id)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:/// _________ '
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

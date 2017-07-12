import requests
import os

ttkey = os.environ['TRANSIT_AND_TRAILS_API_KEY']
ggkey = os.environ['GOOGLE_MAPS_GEOCODE_API_KEY']


def get_geocode(address):
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params={
        "address": address,
        "key": ggkey,
        })

    geocode_result = r.json()

    latitude = geocode_result["results"][0]["geometry"]["location"]["lat"]
    longitude = geocode_result["results"][0]["geometry"]["location"]["lng"]

    return latitude, longitude


def get_dict_of_trails(latitude, longitude, distance):
    """Make api call for local trails."""

    api_base = "https://api.transitandtrails.org/api/v1/trailheads"

    r = requests.get(api_base, params={
        "key": ttkey,
        "latitude": latitude,
        "longitude": longitude,
        "distance": distance
        })

    trails = r.json()

    dict_of_trails = {}

    for trail in trails:
        name = trail["name"]
        latitude = trail["latitude"]
        longitude = trail["longitude"]
        park_name = trail["park_name"]
        trail_id = trail["id"]
        dict_of_trails[name] = [name, latitude, longitude,
                                park_name, trail_id]

    return dict_of_trails


def get_trailhead_info(trail_id):
    """Make api call for trailhead information and return them."""

    api_base = "https://api.transitandtrails.org/api/v1/trailheads"

    r = requests.get(api_base+"/%s" % (trail_id), params={
                     "key": ttkey
                     })

    info = r.json()

    dict_trail_info = {"name": info["name"],
                       "description": info["description"],
                       "trail_id": info["id"],
                       "latitude": info["latitude"],
                       "longitude": info["longitude"],
                       "park_name": info["park_name"]}

    print "################ dict_trail_info: ", dict_trail_info
    return dict_trail_info


def get_trail_attributes(trail_id):
    """Make api call for trail attributes and return them."""

    api_base = "https://api.transitandtrails.org/api/v1/trailheads"

    r = requests.get(api_base+"/%s/attributes" % (trail_id), params={
                     "key": ttkey
                     })

    attributes = r.json()

    list_attributes = []

    for attr in attributes:
        name = attr['name']
        list_attributes.append(name)

    print "################ list_attributes: ", list_attributes
    return list_attributes


def get_trail_photos(trail_id):
    """Make api call for trail photos and return them."""

    api_base = "https://api.transitandtrails.org/api/v1/trailheads"

    r = requests.get(api_base + "/%s/photos" % (trail_id), params={
                     "key": ttkey,
                     })

    photos = r.json()

    list_of_photos = []

    for photo in photos:
        medium_photo = photo['medium']
        list_of_photos.append(medium_photo)
        print "############# medium photo:", medium_photo

    return list_of_photos


def get_trail_maps(trail_id):
    """Make api call for trail maps and return them."""

    api_base = "https://api.transitandtrails.org/api/v1/trailheads"

    r = requests.get(api_base + "/%s/maps" % (trail_id), params={
                     "key": ttkey,
                     })

    trail_maps = r.json()

    list_maps = []

    for maps in trail_maps:
        url = maps['url']
        list_maps.append(url)

    print "############### list_ maps: ", list_maps
    return list_maps

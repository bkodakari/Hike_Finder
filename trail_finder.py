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


def get_list_of_trails(latitude, longitude, distance):
    """Make api call for local trails."""
    r = requests.get("https://api.transitandtrails.org/api/v1/trailheads", params={
        "key": ttkey,
        "latitude": latitude,
        "longitude": longitude,
        "distance": distance
        })

    trails = r.json()

    dict_of_trails = {}
    dict_of_lat_lng = {}

    for trail in trails:
        name = trail['name']
        latitude = trail['latitude']
        longitude = trail['longitude']
        description = trail['description']
        park_name = trail['park_name']
        trail_id = trail['id']
        dict_of_lat_lng[trail_id] = [latitude, longitude]
        dict_of_trails[name] = [name, latitude, longitude, description, park_name, trail_id]

    return [dict_of_trails, dict_of_lat_lng]


def get_trail_attributes(trail_id):
    """Make api call for trail attributes and return them."""
    r = requests.get("https://api.transitandtrails.org/api/v1/trailheads", params={
        "key": ttkey,
        "id": trail_id,
        "attributes": "attributes"
    }
    )

    attributes = r.json()

    return attributes


    # /api/v1/trailheads/[id]/attributes
    # /api/v1/trailheads/[id]/photos
    # /api/v1/trailheads/[id]/maps
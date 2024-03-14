import requests
import os
from opencage.geocoder import OpenCageGeocode
geokey   = os.environ.get('GEOAPIKEY')


def geocode_city(city_name):
    global geokey
    geocoder = OpenCageGeocode(geokey)
    data = geocoder.geocode(city_name)

    lat = data[0]['geometry']["lat"]
    lng = data[0]['geometry']["lng"]
    return lat,lng
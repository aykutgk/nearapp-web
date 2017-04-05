import os
import requests
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ['DJANGO_SETTINGS_MODULE'])
import django
django.setup()

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, Point

google_api_key = settings.GOOGLE_MAP_API_KEY

def get_google_radar_results(lon, lat, radius):
    google_radar_endpoint = "https://maps.googleapis.com/maps/api/place/"\
        "radarsearch/json?location={lat},{lon}&radius={radius}&type=restaurant&"\
        "key={key}".format(lon=lon,lat=lat,radius=radius,key=google_api_key)
    results = []

    try:
        r = requests.get(google_radar_endpoint)
    except Exception as e:
        raise(e)
    else:
        if r.status_code == 200:
            data = r.json()
            if data['status'] == "OK":
                results = data['results']

    return results


def get_google_place_detail(place_id):
    detail = {}
    google_place_detail_endpoint = "https://maps.googleapis.com/maps/api/place/"\
    "details/json?placeid={place_id}&key={key}".format(place_id=place_id, key=google_api_key)

    try:
        r = requests.get(google_place_detail_endpoint)
    except Exception as e:
        raise(e)
    else:
        if r.status_code == 200:
            data = r.json()
            if data['status'] == 'OK':
                data = data['result']
                detail['lon'] = data['geometry']['location']['lng']
                detail['lat'] = data['geometry']['location']['lat']
                detail['name'] = data['name']
                detail['url'] = data['url']
                detail['place_id'] = place_id
    return detail




if __name__ == "__main__":
    from places.models import Place
    from onboarding.models import Owner

    lat = sys.argv[1]
    lon = sys.argv[2]
    radius = sys.argv[3]

    radar_results = get_google_radar_results(lon, lat, radius)

    owner = Owner.objects.get(pk=1)

    for result in radar_results:
        place_detail = get_google_place_detail(result['place_id'])
        try:
            p = Place.objects.create(
                name = place_detail['name'],
                point = Point(place_detail['lon'], place_detail['lat']),
                google_place_id = place_detail['place_id'],
                owner = owner,
                google_map_url = place_detail['url'],
            )
            print(p.id)
        except Exception as e:
            print(e)

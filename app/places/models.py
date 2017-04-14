import logging
import requests

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point

from onboarding.models import Owner


logger = logging.getLogger('django')

"""
class TagCategory(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(TagCategory)

    def __str__(self):
        return self.name


class Channel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
"""


class Place(models.Model):
    owner = models.ForeignKey(Owner, verbose_name="Owner")
    name = models.CharField("Name of the business or place", max_length=255)
    point = models.PointField("Latitude/Longitude on Map", srid=4326)
    google_place_id = models.CharField("Google place id", max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField("Is this business or place still active?", default=True)
    google_map_url = models.URLField("Google map url", blank=True, null=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Place, self).__init__(*args, **kwargs)
        self._distance = 0

    @property
    def lon(self):
        return self.point.x

    @property
    def lat(self):
        return self.point.y

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value.m

    def __get_google_radar_results(lat, lon, radius, google_api_key):
        google_radar_endpoint = "https://maps.googleapis.com/maps/api/place/"\
            "radarsearch/json?location={lat},{lon}&radius={radius}&type=restaurant&"\
            "key={key}".format(lon=lon,lat=lat,radius=radius,key=google_api_key)
        results = []

        try:
            r = requests.get(google_radar_endpoint)
        except Exception as e:
            logger.error(e)
        else:
            if r.status_code == 200:
                data = r.json()
                if data['status'] == "OK":
                    results = data['results']

        return results

    def __get_google_place_detail(place_id, google_api_key):
        detail = {}
        google_place_detail_endpoint = "https://maps.googleapis.com/maps/api/place/"\
        "details/json?placeid={place_id}&key={key}".format(place_id=place_id, key=google_api_key)

        try:
            r = requests.get(google_place_detail_endpoint)
        except Exception as e:
            logger.error(e)
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

    @classmethod
    def save_nearby_places_from_google_place_api(cls, lat=None, lon=None, radius=800):
        """
        Create places by using users current location.
        Results will be coming from Google Place apis
        """
        if lat and lon and radius:
            google_api_key = settings.GOOGLE_MAP_API_KEY_INTERNAL

            try:
                owner = Owner.objects.get(pk=1)
            except Owner.DoesNotExist:
                logger.error("There is no superuser with pk=1")

            radar_results = cls.__get_google_radar_results(lat, lon, radius, google_api_key)

            for result in radar_results:
                place_detail = cls.__get_google_place_detail(result['place_id'], google_api_key)
                try:
                    p = Place.objects.create(
                        name = place_detail['name'],
                        point = Point(place_detail['lon'], place_detail['lat']),
                        google_place_id = place_detail['place_id'],
                        owner = owner,
                        google_map_url = place_detail['url'],
                    )
                except Exception as e:
                    logger.error(e)
        return True

    def __str__(self):
        return self.name

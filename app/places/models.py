from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

from onboarding.models import Owner


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
    point = models.PointField("Longitude/Latitude on Map", default=GEOSGeometry('POINT(0 0)'))
    google_place_id = models.CharField("Google place id", max_length=60, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField("Is this business or place still active?", default=True)

    def __str__(self):
        return self.name

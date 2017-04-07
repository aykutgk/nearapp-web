import logging

from django.contrib.gis.geos import GEOSGeometry, Point

from rest_framework import serializers
from rest_framework.response import Response

from onboarding.models import Owner
from places.models import Place


logger = logging.getLogger('django')


class OwnerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ('id', 'email', 'phone_number', 'first_name', 'last_name', 'password')
        extra_kwargs = {'id': {'read_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = Owner(
            email = validated_data['email'],
            phone_number = validated_data.get('phone_number', None),
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        #user.sms_user("Hi Aykut")
        return user


class PlaceCreateSerializer(serializers.ModelSerializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()

    class Meta:
        model = Place
        fields = ('id', 'name', 'owner', 'google_place_id', 'lon', 'lat', 'google_map_url')
        #exclude = ('point', 'created_at', 'updated_at', 'active')
        extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        place = Place(
            name = validated_data['name'],
            google_place_id = validated_data['google_place_id'],
            owner = validated_data['owner'],
            point = GEOSGeometry(Point(validated_data['lon'], validated_data['lat']))
        )
        place.save()
        return place


class NearbyPlaceCreateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    radius = serializers.IntegerField(min_value=200, max_value=800, default=800)

    def save(self):
        lat = self.validated_data['lat']
        lon = self.validated_data['lon']
        radius = self.validated_data['radius']
        Place.save_nearby_places_from_google_place_api(lat,lon,radius)


class NearbyPlaceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name', 'lon', 'lat', 'google_map_url')
        #exclude = ('point', 'created_at', 'updated_at', 'active')
        extra_kwargs = {'id': {'read_only': True}}

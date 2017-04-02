from django.contrib.gis.geos import GEOSGeometry, Point

from rest_framework import serializers
from rest_framework.response import Response

from onboarding.models import Owner
from places.models import Place



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
        #fields = '__all__'
        exclude = ('id', 'point', 'created_at', 'updated_at', 'active')
        #extra_kwargs = {'id': {'read_only': True}}

    def create(self, validated_data):
        place = Place(
            name = validated_data['name'],
            google_place_id = validated_data['google_place_id'],
            owner = validated_data['owner'],
            point = GEOSGeometry(Point(validated_data['lon'], validated_data['lat']))
        )
        place.save()
        return place

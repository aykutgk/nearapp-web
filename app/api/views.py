import logging

from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D

from places.models import Place

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from onboarding.models import Owner
from .serializers import OwnerCreateSerializer, PlaceCreateSerializer,\
 NearbyPlaceCreateSerializer, NearbyPlaceListSerializer



logger = logging.getLogger('django')


def api_health_check(request):
    return JsonResponse({'ok': True})


class OwnerCreate(generics.CreateAPIView):
    throttle_scope = 'owner_create'
    queryset = Owner.objects.all()
    serializer_class = OwnerCreateSerializer
    permission_class = (permissions.AllowAny,)


class PlaceCreate(generics.CreateAPIView):
    throttle_scope = 'place_create'
    serializer_class = PlaceCreateSerializer
    permission_class = (permissions.AllowAny,)

    def get_serializer_class(self):
        #Namespace Versioning for Api -> logger.error(self.request.version)
        return PlaceCreateSerializer


class NearbyPlaceCreate(generics.CreateAPIView):
    throttle_scope = 'nearby_place_create'
    serializer_class = NearbyPlaceCreateSerializer
    permission_class = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        super(NearbyPlaceCreate, self).create(request, *args, **kwargs)
        return Response({"status": "OK"})


class NearByPlacesPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NearbyPlaceList(generics.ListAPIView):
    queryset = Place.objects.all()
    throttle_scope = 'nearby_place_list'
    serializer_class = NearbyPlaceListSerializer
    permission_class = (permissions.AllowAny,)
    pagination_class = NearByPlacesPagination
    current_lat = None
    current_lon = None
    radius = 800

    def filter_queryset(self, queryset):
        queryset = self.get_queryset()

        if self.current_lat and self.current_lon:
            queryset = queryset.filter(point__isvalid=True)
            queryset = queryset.filter(
                point__distance_lte=(
                    Point(self.current_lon, self.current_lat, srid=4326),
                    D(m=self.radius)
                )
            )

        return queryset

    def list(self, request):
        try:
            self.current_lat = float(self.request.GET['lat'])
            self.current_lon = float(self.request.GET['lon'])
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if 'radius' in self.request.query_params:
            self.radius = int(self.request.GET['radius'])

        return super(NearbyPlaceList, self).list(request)

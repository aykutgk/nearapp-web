from django.conf.urls import url, include

from .views import OwnerCreate, PlaceCreate,\
 NearbyPlaceCreate, NearbyPlaceList, api_health_check


urlpatterns = [
    url(r'^status/$', api_health_check, name="status"),
    url(r'^owner/create/$', OwnerCreate.as_view(), name="owner-create"),
    url(r'^place/create/$', PlaceCreate.as_view(), name="place-create"),
    url(r'^nearby/place/create/$', NearbyPlaceCreate.as_view(), name="nearby-place-create"),
    url(r'^nearby/place/list/$', NearbyPlaceList.as_view(), name="nearby-place-list"),
]

from django.conf.urls import url, include

from .views import OwnerCreate, PlaceCreate, Status


urlpatterns = [
    url(r'^register/owner/$', OwnerCreate.as_view(), name="register-owner"),
    url(r'^register/place/$', PlaceCreate.as_view(), name="register-place"),
    url(r'^status/$', Status, name="status"),
]

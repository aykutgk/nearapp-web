from django.conf.urls import url, include

from .views import OwnerCreate, PlaceCreate


urlpatterns = [
    url(r'^register/owner/$', OwnerCreate.as_view(), name="register-owner"),
    url(r'^register/place/$', PlaceCreate.as_view(), name="register-place"),
]

from django.conf.urls import url, include

from .views import OwnerCreate

app_name = "api-v1"

urlpatterns = [
    url(r'^register/$', OwnerCreate.as_view(), name="register"),
]

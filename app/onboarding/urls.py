from django.conf.urls import url

from .views import OwnerCreate



app_name = "onboarding"

urlpatterns = [
    url(r'^register/$', OwnerCreate.as_view(), name="owner-create")
]

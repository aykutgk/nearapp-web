import logging

from rest_framework import generics
from rest_framework import permissions

from onboarding.models import Owner
from .serializers import OwnerCreateSerializer, PlaceCreateSerializer



logger = logging.getLogger('django')

class OwnerCreate(generics.CreateAPIView):
    throttle_scope = 'register_owner'
    queryset = Owner.objects.all()
    serializer_class = OwnerCreateSerializer
    permission_class = (permissions.AllowAny,)


class PlaceCreate(generics.CreateAPIView):
    serializer_class = PlaceCreateSerializer
    permission_class = (permissions.AllowAny,)

    def get_serializer_class(self):
        #Namespace Versioning for Api -> logger.error(self.request.version)
        return PlaceCreateSerializer

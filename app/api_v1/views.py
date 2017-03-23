from rest_framework import generics
from rest_framework import permissions

from onboarding.models import Owner
from .serializers import OwnerCreateSerializer, PlaceCreateSerializer



class OwnerCreate(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerCreateSerializer
    permission_class = (permissions.AllowAny,)


class PlaceCreate(generics.CreateAPIView):
    serializer_class = PlaceCreateSerializer
    permission_class = (permissions.AllowAny,)

from rest_framework import generics
from rest_framework import permissions

from onboarding.models import Owner
from .serializers import OwnerSerializer



class OwnerCreate(generics.CreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_class = (permissions.AllowAny,)

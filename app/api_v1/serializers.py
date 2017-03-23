from rest_framework import serializers

from onboarding.models import Owner
from places.models import Place



class OwnerSerializer(serializers.ModelSerializer):
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

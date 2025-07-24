from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'username',
            'email',
            'firstname',
            'lastname',
            'profile_image',
            'created',
        ]
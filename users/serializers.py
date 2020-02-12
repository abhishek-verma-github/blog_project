from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
   
    user = UserSerializer(many=False)
    image = serializers.ImageField(
        max_length=None, use_url=True
    )

    class Meta:
        model = Profile
        fields = ['user', 'image']

    def get_image_url(self, obj):
        return obj.image.url

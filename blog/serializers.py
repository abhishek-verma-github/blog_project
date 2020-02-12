from rest_framework import serializers
from .models import Post, Comment
from users.models import Profile
from django.contrib.auth.models import User
from users.serializers import ProfileSerializer, UserSerializer


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    profile = ProfileSerializer(many=False)
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'profile', 'date_posted']
        # fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=False)
    user = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = ['comment', 'post', 'user', 'created_on']

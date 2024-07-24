from rest_framework import serializers
from .models import NewPost

class NewPostSerializer(serializers.ModelSerializer):
    class Meta:
    	model = NewPost
    	fields = ['url', 'title', 'content', 'tag','resource']
from rest_framework import serializers
from .models import Article

class NewArticleSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Article
    	fields = ['url', 'title', 'content', 'tag','resource']
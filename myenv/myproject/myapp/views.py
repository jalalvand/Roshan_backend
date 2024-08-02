from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.permissions import IsAuthenticated

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
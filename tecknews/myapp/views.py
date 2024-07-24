from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import NewPost
from .serializers import NewPostSerializer
from django_filters.rest_framework import DjangoFilterBackend

class NewPostViewSet(viewsets.ModelViewSet):
    queryset = NewPost.objects.all()
    serializer_class = NewPostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag']
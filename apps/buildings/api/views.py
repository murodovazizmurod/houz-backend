from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.buildings.api.serializers import PostListAPISerializer, HotspotAdminSerializer, TerritoryHotspotAdminSerializer
from apps.buildings.models import Post
from apps.territory.models import TerritoryHotspot, Hotspot
from rest_framework.permissions import AllowAny


class PostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListAPISerializer
    ordering_fields = '__all__'
    search_fields = ['name']


class PostChildView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListAPISerializer
    ordering_fields = '__all__'
    search_fields = ['name']


@method_decorator(csrf_exempt, name='dispatch')  # CSRF exemption for testing purposes
class HotspotViewSet(ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotAdminSerializer


@method_decorator(csrf_exempt, name='dispatch')  # CSRF exemption for testing purposes
class TerritoryHotspotViewSet(ModelViewSet):
    queryset = TerritoryHotspot.objects.all()
    serializer_class = TerritoryHotspotAdminSerializer
    permission_classes = [AllowAny]  # Allow all access for testing purposes

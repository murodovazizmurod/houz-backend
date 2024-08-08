from rest_framework import serializers
from .models import Service, Post, Image
from apps.category.models import Category
from apps.territory.serializers import HotspotSerializer, TerritorySerializer
from houz.utils import get_multires

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    panos = serializers.SerializerMethodField()
    multires = serializers.SerializerMethodField()
    panos_preview = serializers.SerializerMethodField()
    panos_thumb = serializers.SerializerMethodField()
    hotspots = HotspotSerializer(many=True, read_only=True)
    territory = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'services', 'size', 'location', 
            'main_image', 'images', 'category', 'panos', 'panos_preview', 
            'panos_thumb', 'multires', 'hotspots', 'territory'
        ]

    def get_panos(self, instance, *args, **kwargs):
        panorama = instance.panorama
        if not panorama:
            return None
        path, ext = str(panorama.url).split(".")
        pano_path = ".tiles/%s/l%l/%v/l%l_%s_%v_%h.jpg"
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        return "%s%s%s" % (base_url, path, pano_path)

    def get_multires(self, instance, *args, **kwargs):
        panorama = instance.panorama
        if not panorama:
            return None
        path, ext = str(panorama.url).split(".")
        tour_path = path + ".tiles/tour.xml"
        return get_multires(tour_path)

    def get_panos_preview(self, instance, *args, **kwargs):
        panorama = instance.panorama
        if not panorama:
            return None
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/preview.jpg")

    def get_panos_thumb(self, instance, *args, **kwargs):
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        panorama = instance.panorama
        if not panorama:
            if instance.video_preview:
                return "%s%s" % (base_url, instance.video_preview.url)
            elif instance.video_thumb:
                return "%s%s" % (base_url, instance.video_thumb.url)
            return None
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/thumb.jpg")
    
    def get_territory(self, instance):
        if instance.parent:
            territory = instance.parent.territories.first()
        else:
            territory = instance.territories.first()
        if territory:
            return TerritorySerializer(instance=territory, context=self.context).data
        return None

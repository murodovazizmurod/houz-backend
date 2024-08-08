from rest_framework import serializers

from houz.utils import get_multires
from apps.buildings.models import Post
from apps.territory.models import TerritoryHotspot, Hotspot


class PostListAPISerializer(serializers.ModelSerializer):
    panos = serializers.SerializerMethodField()
    multires = serializers.SerializerMethodField()
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "panorama",
            "panos",
            "thumb",
            "multires",
        )

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

    def get_thumb(self, instance, *args, **kwargs):
        panorama = instance.panorama
        if not panorama:
            return None
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/thumb.jpg")


class HotspotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotspot
        fields = (
            "id",
            "src",
            "post",
            "h",
            "v",
            "index"
        )


class TerritoryHotspotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerritoryHotspot
        fields = (
            "territory",
            "post",
            "h",
            "v",
            "index"
        )



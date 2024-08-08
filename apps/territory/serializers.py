from rest_framework import serializers

from apps.territory.models import Territory, TerritoryHotspot
from apps.buildings.models import Post
from apps.territory.models import Hotspot
from apps.category.serializers import CategorySerializer
from houz.utils import get_multires_flat


class TerritorySerializer(serializers.ModelSerializer):
    panos = serializers.SerializerMethodField()
    multires = serializers.SerializerMethodField()
    panos_preview = serializers.SerializerMethodField()
    panos_thumb = serializers.SerializerMethodField()

    class Meta:
        model = Territory
        fields = (
            "id",
            "name",
            "description",
            "image",
            "panos",
            "panos_preview",
            "panos_thumb",
            "multires",
        )

    def get_panos(self, instance, *args, **kwargs):
        image = instance.image
        if not image:
            return None
        path, ext = str(image.url).split(".")
        pano_path = ".tiles/l%l/%v/l%l_%v_%h.jpg"
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        return "%s%s%s" % (base_url, path, pano_path)

    def get_multires(self, instance, *args, **kwargs):
        image = instance.image
        if not image:
            return None
        path, ext = str(image.url).split(".")
        tour_path = path + ".tiles/tour.xml"
        return get_multires_flat(tour_path)

    def get_panos_preview(self, instance, *args, **kwargs):
        panorama = instance.image
        if not panorama:
            return None
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/preview.jpg")

    def get_panos_thumb(self, instance, *args, **kwargs):
        image = instance.image
        if not image:
            return None
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        path, ext = str(image.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/thumb.jpg")


class PostShortListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    panos_preview = serializers.SerializerMethodField()
    thumb = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "category",
            "thumb",
            "panos_preview",
        )

    def get_panos_preview(self, instance, *args, **kwargs):
        panorama = instance.panorama
        if not panorama:
            return None
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/preview.jpg")

    def get_thumb(self, instance, *args, **kwargs):
        request = self.context["request"]
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        panorama = instance.panorama
        if not panorama:
            if instance.video_preview:
                return "%s%s" % (base_url, instance.video_preview.url)
            elif instance.video_thumb:
                return "%s%s" % (base_url, instance.video_preview.url)
            return None
        path, ext = str(panorama.url).split(".")
        return "%s%s%s" % (base_url, path, ".tiles/thumb.jpg")


class HotspotSerializer(serializers.ModelSerializer):
    src = PostShortListSerializer(read_only=True)

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


class TerritoryHotspotSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer(read_only=True)

    class Meta:
        model = TerritoryHotspot
        fields = (
            "post",
            "territory",
            "h",
            "v",
            "index"
        )


class TerritoryHotspotListSerializer(serializers.ModelSerializer):
    post = PostShortListSerializer(read_only=True)

    class Meta:
        model = TerritoryHotspot
        fields = (
            "post",
            "territory",
            "h",
            "v",
            "index"
        )

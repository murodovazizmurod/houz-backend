from django.shortcuts import render

from houz.utils import get_multires_flat
from apps.category.models import Category
from apps.territory.models import Territory, Hotspot, TerritoryHotspot
from apps.territory.serializers import HotspotSerializer, TerritoryHotspotListSerializer, TerritorySerializer
from apps.territory.filters import TerritoryHotspotFilter

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def view_territory(request, id):
    territory = Territory.objects.get(id=id)
    categories = Category.objects.all()
    path, ext = str(territory.image.url).split(".")
    pano_path = ".tiles"
    panorama_path = "%s%s" % (path, pano_path)
    path, ext = str(territory.image.url).split(".")
    tour_path = path + ".tiles/tour.xml"
    multires = get_multires_flat(tour_path)
    return render(request, "place/territory.html", {
        "territory": territory,
        "flat_path": panorama_path,
        "multires": multires,
        "categories": categories,
        "hotspots": territory.hotspots.all(),
    })


class HotspotViewSet(ModelViewSet):
    queryset = Hotspot.objects.all()
    serializer_class = HotspotSerializer


class TerritoryHotspotViewSet(ModelViewSet):
    queryset = TerritoryHotspot.objects.all()
    serializer_class = TerritoryHotspotListSerializer
    pagination_class = None
    filterset_class = TerritoryHotspotFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        hotspots = serializer.data
        territory = request.query_params.get('territory')
        try:
            territory = Territory.objects.get(id=territory)
        except Territory.DoesNotExist:
            territory = None
        result = {"hotspots": hotspots}
        return Response(result)

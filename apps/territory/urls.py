from django.urls import include, path

from apps.buildings import views
# project
from apps.territory.views import view_territory
from apps.territory.views import TerritoryHotspotViewSet

urlpatterns = [
    path(
        "territory/tour/<int:id>/",
        view_territory,
        name="view_territory",
    ),
    path("territory-hotspot/", TerritoryHotspotViewSet.as_view({"get": "list"})),
    path(
        "place/place_place/<int:id>/",
        views.view_tour,
        name="view_tour",
    ),
]

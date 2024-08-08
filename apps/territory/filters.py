import django_filters
from apps.territory.models import TerritoryHotspot



class TerritoryHotspotFilter(django_filters.FilterSet):
    class Meta:
        model = TerritoryHotspot
        fields = (
            "territory",
        )

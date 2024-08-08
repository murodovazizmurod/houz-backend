import django_filters


from apps.buildings.models import Post
from apps.territory.models import TerritoryHotspot


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = (
            'category',
            'city',
            'is_main',
            'show_in_map'
        )

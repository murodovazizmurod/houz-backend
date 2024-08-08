import random
import string

from django.conf import settings
from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe


from houz import krpano
from apps.territory.models import Territory, Hotspot, TerritoryHotspot


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "image_tag",
        "territory_show",
    )
    search_fields = [
        "name"
    ]

    def territory_show(self, obj):
        url = reverse("view_territory", args=[obj.id])
        return mark_safe(f'<a href="{url}" class="button">{"Смотреть"}</a>')

    territory_show.short_description = "Территория"
    territory_show.allow_tags = True

    def image_tag(self, obj):
        if obj.image is not None:
            return mark_safe('<img src="{}" style="width:50px;height:50px;"/>'.format(obj.image.url))
        else:
            return ""

    image_tag.short_description = "Фото"
    image_tag.allow_tags = True

    def save_model(self, request, obj, form, change):
        old_image = form.initial.get("image")
        old_image_url = None
        if old_image:
            old_image_url = old_image.url
        super().save_model(request, obj, form, change)
        if 'image' in form.changed_data:
            new_panorama_url = obj.image.url
            krpano.flat_tile(new_panorama_url, old_image_url)

@admin.register(Hotspot)
class HotspotAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "src",
        "h",
        "v"
    )


@admin.register(TerritoryHotspot)
class TerritoryHotspotAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "territory",
        "h",
        "v"
    )


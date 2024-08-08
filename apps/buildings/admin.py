from django.contrib import admin
from .models import Service, Post, Image
from django.utils.html import mark_safe
from houz import krpano

class ImageInline(admin.TabularInline):
    model = Post.images.through
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'size', 'location', 'category']
    list_filter = ['category']
    search_fields = ['title', 'description']
    filter_horizontal = ['services']
    inlines = [ImageInline]

    def save_model(self, request, obj, form, change):
        # generate panorama images with krpano
        old_panorama = form.initial.get("panorama")
        old_panorama_url = None
        if old_panorama:
            old_panorama_url = old_panorama.url
        super().save_model(request, obj, form, change)
        if 'panorama' in form.changed_data:
            new_panorama_url = obj.panorama.url
            krpano.tile_full(new_panorama_url, old_panorama_url)
            

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag']
    search_fields = ['image']

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image_url}" width="100" height="100" />')
        return "-"
    image_tag.short_description = 'Image'
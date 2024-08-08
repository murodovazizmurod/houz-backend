import uuid
from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from apps.category.models import Category
from apps.buildings.models import Post


def upload_panorama(instance, filename):
    file_type = filename.split('.')[-1]
    today = str(datetime.today())[0:7]
    try:
        RegexValidator(r'^(jpg|jpeg|JPG)$').__call__(file_type)
        return 'flat/%s/%s.%s' % (
            today, uuid.uuid4(), file_type)
    except ValidationError:
        raise ValidationError(_('Invalid file type'))


class Territory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="territories")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_panorama)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('территория')
        verbose_name_plural = _('территории')


class Hotspot(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="hotspots")
    src = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="srcs")
    h = models.FloatField()
    v = models.FloatField()
    index = models.FloatField(null=True, blank=True)


class TerritoryHotspot(models.Model):
    post = models.OneToOneField(
        Post,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="territory_hotspot",
    )
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name="hotspots")
    h = models.FloatField()
    v = models.FloatField()
    index = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("post", "territory")

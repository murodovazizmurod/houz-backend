from django.db import models
from apps.category.models import Category

import uuid
from datetime import datetime
from django.core.validators import (
    MaxValueValidator,
    RegexValidator,
    ValidationError
)


def upload_panorama(instance, filename):
    file_type = filename.split('.')[-1]
    today = str(datetime.today())[0:7]
    try:
        RegexValidator(r'^(jpg|jpeg|JPG)$').__call__(file_type)
        return 'panorama/%s/%s.%s' % (
            today, uuid.uuid4(), file_type)
    except ValidationError:
        raise ValidationError(('Invalid file type'))
    

class Service(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    services = models.ManyToManyField(Service)
    size = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    main_image = models.ImageField(upload_to='images/')
    images = models.ManyToManyField('Image', related_name='post_images')
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    panorama = models.ImageField("Panorama", null=True, blank=True, upload_to=upload_panorama)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="родитель"
    )

    def __str__(self):
        return self.title

class Image(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.image)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""

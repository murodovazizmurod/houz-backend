from django.http import HttpResponse
from django.conf import settings
import os

def serve_image(request, image_name):
    file_path = os.path.join(settings.IMAGES_ROOT, image_name)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content_type = 'image/jpeg'  # Default to JPEG, adjust if needed
            if image_name.lower().endswith('.png'):
                content_type = 'image/png'
            elif image_name.lower().endswith('.gif'):
                content_type = 'image/gif'
            return HttpResponse(f.read(), content_type=content_type)
    else:
        return HttpResponse(status=404)

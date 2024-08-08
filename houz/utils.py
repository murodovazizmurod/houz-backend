import uuid
import xml.etree.ElementTree as ET
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.conf import settings


FILE_TYPES = {
    r'^(jpg|jpeg|png|gif|JPG|webp|svg)$': 'image',
    r'^(pdf)$': 'pdf',
    r'^(doc|docx|ppt)$': 'document',
    r'^(xlsx|xls)$': 'excel',
    r'^(mp4|webm|m4v|M4V)$': 'video',
    r'^(mp3)$': 'audio'
}


def upload_media_path(instance, filename):
    f_name, *args, file_type = filename.split('.')
    today = str(datetime.today())[0:7]
    print(file_type)
    for regex, folder in FILE_TYPES.items():
        try:
            RegexValidator(regex).__call__(file_type)
            return '%s/%s/%s.%s' % (
                folder, today, uuid.uuid4(), file_type)
        except ValidationError as e:
            pass
            # raise ValidationError(_('Invalid file type'))


def get_multires(path: str) -> str:
    workdir = settings.BASE_DIR
    tour_path = str(workdir) + path
    tree = ET.parse(tour_path)
    try:
        root = tree.getroot()
        attrs = root[2].find("image").find("cube").attrib
        multires = attrs['multires']
    except Exception:
        multires = None
    return multires


def get_multires_flat(path: str) -> str:
    workdir = settings.BASE_DIR
    tour_path = str(workdir) + path
    tree = ET.parse(tour_path)
    try:
        root = tree.getroot()
        attrs = root[2].find("image").find("flat").attrib
        multires = attrs['multires']
    except Exception:
        multires = None
    return multires


def environment_callback(request):
    if settings.DEBUG:
        return [_("Development"), "info"]

    return [_("Production"), "warning"]


def linkify(field_name):
    """
    Converts a foreign key value into clickable links.

    If field_name is 'parent', link text will be str(obj.parent)
    Link will be admin url for the admin url for obj.parent.id:change
    """

    def _linkify(obj):
        linked_obj = getattr(obj, field_name)
        if linked_obj is None:
            return '-'
        app_label = linked_obj._meta.app_label
        model_name = linked_obj._meta.model_name
        view_name = f'admin:{app_label}_{model_name}_change'
        link_url = reverse(view_name, args=[linked_obj.pk])
        return format_html('<a href="{}">{}</a>', link_url, linked_obj)

    _linkify.short_description = field_name  # Sets column name
    return _linkify


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.m4v', '.M4V', '.MP4', '.mov', '.avi', '.wmv', '.avchd', '.webm', '.flv', 'MPEG']
    return ext.lower() in valid_extensions

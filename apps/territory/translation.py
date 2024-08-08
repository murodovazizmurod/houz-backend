from modeltranslation.translator import register, TranslationOptions
from apps.territory.models import Territory, Floor


@register(Territory)
class TerritoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Floor)
class FloorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

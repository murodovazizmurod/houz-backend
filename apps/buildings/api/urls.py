from django.urls import path, include
from rest_framework import routers

# project
from apps.buildings.api import views

router = routers.DefaultRouter()
router.register(r"hotspot", views.HotspotViewSet, basename="hotspot")
router.register(r"territory-hotspot", views.TerritoryHotspotViewSet, basename="territory-hotspot")

urlpatterns = [
    path("", include(router.urls)),
    path("post/", views.PostView.as_view()),
    path("post/children/", views.PostChildView.as_view()),
]

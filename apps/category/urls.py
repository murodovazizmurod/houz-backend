from django.urls import path
from .views import CategoryListView

urlpatterns = [
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
]


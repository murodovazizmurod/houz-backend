from django.urls import path, include
from .views import PostListView, PostDetailView, PostsByCategoryView

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='post-list'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/categories/<int:pk>/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('api/', include('apps.buildings.api.urls'))
]

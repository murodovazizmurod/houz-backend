from rest_framework import generics
from .models import Category, Post
from django.urls import reverse
from .serializers import PostSerializer
from django.shortcuts import render, redirect
from houz.utils import get_multires
from django.db.models import Value, IntegerField
from django.contrib.admin.views.decorators import staff_member_required



class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostsByCategoryView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Post.objects.filter(category_id=category_id)


@staff_member_required
def view_tour(request, id):
    post = Post.objects.get(id=id)
    if not post.panorama:
        if post.parent:
            url = '{}?parent__pk__exact={}'.format(reverse("admin:post_subpost_changelist"), post.parent.id)
            return redirect(url)
        else:
            return redirect(reverse("admin:post_post_changelist"))

    path, ext = str(post.panorama.url).split(".")
    pano_path = ".tiles"
    panorama_path = "%s%s" % (path, pano_path)
    path, ext = str(post.panorama.url).split(".")
    tour_path = path + ".tiles/tour.xml"
    multires = get_multires(tour_path)
    categories = Category.objects.all()
    return render(request, 'place/place.html', {
        "post": post,
        "panorama_path": panorama_path,
        "multires": multires,
        "categories": categories,
        "hotspots": post.hotspots.all()
    })

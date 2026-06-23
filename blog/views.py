from django.shortcuts import render, get_object_or_404, redirect

from .models import Post


def index(request):
    return render(request, 'home.html')


def blog_view(request):
    posts = Post.objects.prefetch_related("tags").all()
    return render(request, "template_name", {"posts": posts}) # change template name


def post_view(request, slug):
    queryset = Post.objects.prefetch_related("tags", "chapters")
    post = get_object_or_404(queryset, slug=slug)
    return render(request, 'template_name', {"post": post}) # change template name


def contacts_view(request):
    return render(request, 'contacts_page.html')

from django.shortcuts import render, get_object_or_404

from .models import Post


def index(request):
    return render(request, 'home.html')


def blog_view(request):
    searching = request.GET.get("q", "").strip()
    tag = request.GET.get("tag", "").strip()
    
    if searching and tag:
        posts = Post.objects.prefetch_related("tags").filter(tags__name=tag, title__icontains=searching)
    elif searching:
        posts = Post.objects.prefetch_related("tags").filter(title__icontains=searching)
    elif tag:
        posts = Post.objects.prefetch_related("tags").filter(tags__name=tag)
    else:
        posts = Post.objects.prefetch_related("tags").all()
        
    context = {
        "posts": posts,
        "search_query": searching,
        "current_tag": tag,
    }
    
    return render(request, "blog.html", context)


def post_view(request, slug):
    queryset = Post.objects.prefetch_related("tags", "chapters")
    post = get_object_or_404(queryset, slug=slug)
    return render(request, 'single-post.html', {"post": post})


def contacts_view(request):
    return render(request, 'contacts_page.html')

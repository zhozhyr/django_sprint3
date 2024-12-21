from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .models import Post, Category


def filter_posts():
    filtered_posts = (
        Post.objects.select_related(
            "category",
            "location",
            "author",
        )
        .filter(
            pub_date__lte=now(),
            is_published = True,
            category__is_published = True,
        ).order_by('-pub_date')[:5]
    )

    return filtered_posts


def index(request):
    posts = filter_posts()
    return render(request, 'blog/index.html', {'post_list': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(
            pub_date__lte=now(),
            is_published=True,
            category__is_published=True
        ).select_related('category', 'author'),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts = (
        Post.objects.filter(
            is_published=True,
            pub_date__lte=now(),
            category=category
        ).select_related('author').order_by('-pub_date')
    )

    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, 'blog/category.html', context)

from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import Post, Category
from .utils import mk_paginator


def home(request):
    news = Post.objects.all()
    latest_stories = news[:2]
    latest_politics = news.filter(category__title='Politics')[:4]
    latest_news = news.filter(category__title='News')[:4]
    latest_features = news.filter(category__title='Features')[:7]
    latest_opinions = news.filter(category__title='Opinion')[:3]
    latest_sports = news.filter(category__title='Sports')[:4]
    latest_personality = news.filter(category__title='Personality')[:6]
    latest_world = news.filter(category__title='World')[:8]
    latest_africa = news.filter(category__title='Africa')[:8]
    latest_economy = news.filter(category__title='Economy')[:4]
    latest_entertainment = news.filter(category__title='Entertainment')[:4]
    latest_security = news.filter(category__title='Security')[:4]
    latest_columnists = news.filter(category__title='Columnists')[:1]

    template = 'home.html'
    context = {
        'latest_politics': latest_politics,
        'latest_stories': latest_stories,
        'latest_news': latest_news,
        'latest_features': latest_features,
        'latest_opinions': latest_opinions,
        'latest_sports': latest_sports,
        'latest_personality': latest_personality,
        'latest_africa': latest_africa,
        'latest_world': latest_world,
        'latest_economy': latest_economy,
        'latest_entertainment': latest_entertainment,
        'latest_security': latest_security,
        'latest_columnists': latest_columnists,
    }

    return render(request, template, context)


def post(request, slug):
    
    post = get_object_or_404(Post, slug=slug)

    similar_posts = Post.objects.filter(category=post.category.id).exclude(id=post.id)[:4]

    return render(request,
                  'post.html',
                  {'post': post,
                   'similar_posts': similar_posts})


def contact(request):

    template = 'contact.html'
    context = {}

    return render(request, template, context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all()
    posts = mk_paginator(request, posts, 10)
    
    template = 'category.html'
    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, template, context)


def post_search(request):
    posts = ''
    query = request.GET.get('q', None)
    post_count = 0
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        post_count = posts.count()
    context = {
        'posts': posts,
        'query': query,
        'post_count': post_count,
    }

    return render(request,
                  'search.html', context)

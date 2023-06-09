from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import Count
from taggit.models import Tag
from .models import Post, Category, Comment
from .forms import CommentForm
from .utils import mk_paginator


def home(request):
    news = Post.objects.all()
    latest_stories = news[:2]
    latest_politics = news.filter(category__title='Politics')[:4]
    latest_news = news.filter(category__title='News')[:4]
    latest_features = news.filter(category__title='Features')[:7]
    latest_opinions = news.filter(category__title='Opinion')[:3]
    latest_sports = news.filter(category__title='Sports')[:4]
    latest_personality = news.filter(category__title='Personality')[:4]
    latest_world = news.filter(category__title='World')[:8]
    latest_africa = news.filter(category__title='Africa')[:8]
    latest_economy = news.filter(category__title='Economy')[:4]
    latest_entertainment = news.filter(category__title='Entertainment')[:4]
    latest_security = news.filter(category__title='Security')[:4]
    latest_editorial = news.filter(category__title='Editorial')[:1]
    popular_news = Post.objects.order_by('-page_views')[:4]
    latest_interview = news.filter(category__title='Interview')[:1]

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
        'latest_editorial': latest_editorial,
        'popular_news': popular_news,
        'latest_interview': latest_interview,
    }

    return render(request, template, context)


def post(request, slug):
    
    post = get_object_or_404(Post, slug=slug)
    similar_posts = Post.objects.filter(category=post.category.id).exclude(id=post.id)[:4]
    comments = post.comments.filter(is_public=True)

    # Create a session key for a visitor
    session_key = 'viewed_post_{}'.format(post.pk)
    if not request.session.get(session_key, False):
        post.page_views += 1
        post.save()
        request.session[session_key] = True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment was posted successfully.')
            return redirect(post)
        else:
            messages.warning(request, 'An error occured while trying to post comment.')
    else:
        form = CommentForm()

    return render(request,
                  'post.html',
                  {'post': post,
                   'similar_posts': similar_posts,
                   'form': form,
                   'comments': comments})


def archive(request):
    news = Post.objects.all()
    template = 'archive.html'
    context = {'news': news}

    return render(request, template, context)


def contact(request):

    template = 'contact.html'
    context = {}

    return render(request, template, context)


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.all()
    posts = mk_paginator(request, posts, 10)
    # Retrieve top categories by post count
    top_categories = Category.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    # Get the number of posts for each top category
    top_categories_with_count = [(cat, cat.post_count) for cat in top_categories]
    # Retrieve most popular news posts in the category based on page views
    popular_posts = category.posts.order_by('-page_views')[:5]
    
    template = 'category.html'
    context = {
        'category': category,
        'posts': posts,
        'top_categories': top_categories_with_count,
        'popular_posts': popular_posts,
    }

    return render(request, template, context)


def search(request):
    posts = ''
    query = request.GET.get('q', None)
    if query:
        posts = Post.objects.filter(title__icontains=query)
    context = {
        'posts': posts,
        'query': query,
    }

    return render(request,
                  'search.html', context)


def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags__in=[tag])
    posts = mk_paginator(request, posts, 10)
    
    template = 'tag.html'
    context = {
        'tag': tag,
        'posts': posts,
    }

    return render(request, template, context)


def error_500(request):
    return render(request, "500.html")


def error_404(request, exception):
    return render(request, "404.html")

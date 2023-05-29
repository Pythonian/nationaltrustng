from .models import Category, Post


def categories(request):
    return {
        'categories': Category.objects.all()[:12]
        }

def latest_news(request):
    return {
        'latest_news': Post.objects.all()[:5]
    }
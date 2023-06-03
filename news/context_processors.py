from .models import Category, Post


def categories(request):
    return {
        'categories': Category.objects.all()[:12]
        }

def breaking_news(request):
    return {
        'breaking_news': Post.objects.all()[:5]
    }
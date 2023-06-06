from .models import Category, Post


def categories(request):
    return {
        'categories': Category.objects.all()
        }

def breaking_news(request):
    return {
        'breaking_news': Post.objects.all()[:5]
    }
from django import template
from news.utils import get_youtube_thumbnail_url

register = template.Library()

@register.filter
def youtube_thumbnail(url):
    return get_youtube_thumbnail_url(url)

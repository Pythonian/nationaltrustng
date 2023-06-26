from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.contrib.sitemaps import ping_google
from taggit.managers import TaggableManager
from .utils import get_read_time


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.SmallIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:category', args=[self.slug])


class Post(models.Model):
    title = models.CharField(_('title'), max_length=250)
    slug = models.SlugField(_('slug'), max_length=250,
                            unique_for_date='created')
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.PROTECT,
                                 verbose_name=_('category'),
                                 related_name='posts')
    body = RichTextUploadingField(_('body'), blank=True, null=True)
    image = models.ImageField(upload_to='posts_images',
                              verbose_name=_('image'),
                              blank=True, null=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(960, 520)],
                                     format='JPEG', options={'quality': 60})
    image_link = models.URLField(blank=True, null=True, help_text='Enter Image URL here.')
    image_caption = models.CharField(_('image caption'),
                                     blank=True, max_length=50)
    created = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now=True)
    page_views = models.PositiveIntegerField(
        _('page views'), default=0)
    read_time = models.PositiveIntegerField(
        _('read time'), default=0,
        help_text='Estimated time taken to read the post.')
    tags = TaggableManager()


    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('news:post',
                       args=[self.slug])

    def get_previous_post(self):
        return self.get_previous_by_created()

    def get_next_post(self):
        return self.get_next_by_created()

    def save(self, *args, **kwargs):

        if self.body:
            self.read_time = get_read_time(self.body)

        super().save(*args, **kwargs)

        # Ping google due to sitemap changes that
        # arises from a new Post being created.
        try:
            ping_google()
        except Exception:
            pass

    @property
    def word_count(self):
        return len(strip_tags(self.body).split())
    

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='galleries')
    image = models.ImageField(upload_to='posts_images/extra', blank=True, null=True)
    image_caption = models.CharField(_('image caption'),
                                     blank=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True, help_text='Uncheck this if you do not want this comment to appear on the site.')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
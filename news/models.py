import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.sitemaps import ping_google
from .utils import get_read_time

content_validator = MinLengthValidator(
    limit_value=300, message="Content should be at least 300 characters long!")


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name=_('author'),
                               related_name='posts')
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.PROTECT,
                                 verbose_name=_('category'),
                                 related_name='posts')
    body = RichTextUploadingField(_('body'), validators=[content_validator])
    image = models.ImageField(upload_to='posts_images',
                              verbose_name=_('image'), default='post.png')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(960, 520)],
                                     format='JPEG', options={'quality': 60})
    image_caption = models.CharField(_('image caption'),
                                     blank=True, max_length=50)
    created = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now=True)
    page_views = models.PositiveIntegerField(
        _('page views'), default=0)
    read_time = models.PositiveIntegerField(
        _('read time'), default=0,
        help_text='Estimated time taken to read the post.')


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

    def get_page_views_last_week(self):
        """Calculates the number of page views for a post in the last 7 days"""
        cutoff = timezone.now() - timezone.timedelta(days=7)
        # count the number of page views that occured after the cutoff date
        views = self.post.filter(created__gte=cutoff).count()
        return views

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

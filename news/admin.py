from django.contrib import admin
from django.http import HttpResponseRedirect
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category, Comment, Post
from .twitter import post_tweet


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['category', 'created']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['-created']
    inlines = [CommentInline]

    def change_view(self, request, object_id, extra_context=None):
        """ Override the page admin is directed to after saving a post."""
        result = super().change_view(request, object_id, extra_context)
        post = Post.objects.get(id__iexact=object_id)
        if not request.POST.__contains__('_addanother') and not request.POST.__contains__('_continue'):
            result['Location'] = post.get_absolute_url()
        return result
    
    def add_view(self, request, form_url='', extra_context=None):
        # Save the new post
        response = super().add_view(request, form_url, extra_context)
        if isinstance(response, HttpResponseRedirect):
            # Retrieve the saved post object
            post = self.model.objects.latest('id')
            # Construct a new redirect response with the desired URL
            redirect_url = post.get_absolute_url()
            response = HttpResponseRedirect(redirect_url)
        return response

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     if not change:
    #         post_tweet(obj)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class FlatPageCustom(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created']
    list_filter = ['category', 'created', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    ordering = ['-created']

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
    
    # def add_view(self, request, form_url='', extra_context=None):
    #     # Save the new post
    #     response = super().add_view(request, form_url, extra_context)
    #     if isinstance(response, HttpResponseRedirect):
    #         # Retrieve the saved post object
    #         post = self.model.objects.latest('id')
    #         # Redirect to the post's get_absolute_url page
    #         response.url = post.get_absolute_url()
    #     return response


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

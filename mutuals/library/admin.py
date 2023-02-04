from django.contrib import admin
from .models import Interest, Post, Comment, SiteUser


class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_name', 'created')
    search_fields = ('post_name',)
    filter_horizontal = ('interest_tag',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'body')


class SiteUserAdmin(admin.ModelAdmin):
    list_display = ('page_user', 'about')
    search_fields = ('page_user', 'about')


admin.site.register(Interest, InterestAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SiteUser, SiteUserAdmin)

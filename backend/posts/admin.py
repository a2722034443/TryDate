from django.contrib import admin
from .models import Post, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'is_anonymous', 'content', 'like_count', 'status', 'created_at']
    list_filter = ['status', 'is_anonymous']
    search_fields = ['author__nickname', 'content']

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']

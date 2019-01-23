from django.contrib import admin
from .models import Post, Comment, LikeModel, Follow


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'picture', 'context')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'context', 'parent', 'created_at')


@admin.register(LikeModel)
class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'status', 'created_at')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')

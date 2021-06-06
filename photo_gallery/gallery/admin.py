from django.contrib import admin

from .models import Album, Photo, Comment, Bookmark


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('description', 'album', 'owner', 'photo', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('photo', 'text', 'owner', )


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('photo', 'owner', )

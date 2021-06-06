from django.urls import path

from api.views import (
    FeedApi,
    SignupApi,
    AlbumApi,
    AlbumRetrieveUpdateDestroyApi,
    PhotoApi,
    PhotoRetrieveUpdateDestroyApi,
    UserPhotosApi,
    UserAlbumsApi,
    CommentApi,
    CommentDeleteApi,
    BookmarkApi,
    BookmarksListApi,
    BookmarkDeleteApi,
    UserApi,
    UserIdApi,
    UserBookmarksApi,
)

app_name = "v1"

urlpatterns = [
    path("signup/", SignupApi.as_view(), name="signup"),
    path("albums/", AlbumApi.as_view(), name="albums"),
    path("album/<int:pk>/", AlbumRetrieveUpdateDestroyApi.as_view(), name="album"),
    path("photos/", PhotoApi.as_view(), name="photos"),
    path("photo/<int:pk>/", PhotoRetrieveUpdateDestroyApi.as_view(), name="photo"),
    path("user/<int:user_pk>/photos/", UserPhotosApi.as_view(), name="user_photos"),
    path("user/<int:user_pk>/albums/", UserAlbumsApi.as_view(), name="user_albums"),
    path(
        "user/<int:user_pk>/bookmarks/",
        UserBookmarksApi.as_view(),
        name="user_bookmarks",
    ),
    path("photo/<int:photo_pk>/comments/", CommentApi.as_view(), name="photo_comments"),
    path(
        "photos/comment/delete/<int:pk>/",
        CommentDeleteApi.as_view(),
        name="comment_delete",
    ),
    path("bookmark/<int:photo_pk>/", BookmarkApi.as_view(), name="bookmark"),
    path("bookmarks/", BookmarksListApi.as_view(), name="bookmarks"),
    path(
        "bookmark/delete/<int:pk>/", BookmarkDeleteApi.as_view(), name="bookmark_delete"
    ),
    path("feed/", FeedApi.as_view(), name="feed"),
    path("user/me/", UserApi.as_view(), name="user"),
    path("user/<int:pk>/", UserIdApi.as_view(), name="user_id"),
]

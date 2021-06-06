import pytest
from model_bakery import baker

from api.serializers import (
    AlbumSerializer,
    PhotoSerializer,
    CommentSerializer,
    BookmarkSerializer,
)
from gallery.models import Album, Bookmark, Comment

pytestmark = pytest.mark.django_db


class TestAlbumSerializer:
    @pytest.mark.unit
    def test_serialize_model(self):
        album = baker.make("gallery.Album")
        serializer = AlbumSerializer(album)
        assert serializer.data

    def test_serialize_data(self, client, create_user):
        user = create_user()
        client.force_login(user=user)
        album = Album.objects.create(name="album", owner=user)
        serializer = AlbumSerializer(
            data={"id": album.id, "name": album.name, "user": album.owner}
        )
        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_serialize_data_error(self, client, create_user, create_user_1):
        user_1 = create_user_1()
        user = create_user()
        client.force_login(user=user)
        album = Album.objects.create(name="album", owner=user)
        serializer = AlbumSerializer(
            data={"id": album.id, "name": album.name, "user": user_1}
        )
        assert not serializer.is_valid()
        assert serializer.errors


class TestPhotoSerializer:
    @pytest.mark.unit
    def test_serialize_model(self):
        photo = baker.make("gallery.Photo")
        serializer = PhotoSerializer(photo)
        assert serializer.data


class TestCommentSerializer:
    @pytest.mark.unit
    def test_serialize_model(self):
        comment = baker.make("gallery.Comment")
        serializer = CommentSerializer(comment)
        assert serializer.data

    def test_serialize_data(self):
        photo = baker.make("gallery.Photo")
        comment = {"id": 1, "text": "album name", "photo": photo.id, "user": 1}
        serializer = CommentSerializer(data=comment)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    def test_serialize_data_error(self, client, create_user):
        user = create_user()
        client.force_login(user=user)
        photo = baker.make("gallery.Photo", owner=user)
        photo_1 = baker.make("gallery.Photo")
        comment = Comment.objects.create(owner=user, text="comment", photo=photo_1)
        serializer = CommentSerializer(
            data={
                "id": comment.id,
                "text": "comment",
                "user": user,
                "photo": photo_1.id,
            }
        )
        assert not serializer.is_valid()
        assert serializer.errors
        serializer = CommentSerializer(
            data={
                "id": comment.id,
                "text": comment.text,
                "user": user,
                "photo": photo.id,
            }
        )
        assert not serializer.is_valid()
        assert serializer.errors


class TestBookmarkSerializer:
    @pytest.mark.unit
    def test_serialize_model(self):
        bookmark = baker.make("gallery.Bookmark")
        serializer = BookmarkSerializer(bookmark)
        assert serializer.data

    def test_serialize_data(self):
        photo = baker.make("gallery.Photo")
        bookmark = {"id": 1, "photo": photo.id, "user": 1}
        serializer = BookmarkSerializer(data=bookmark)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    def test_serialize_data_error(self, client, create_user):
        user = create_user()
        client.force_login(user=user)
        photo = baker.make("gallery.Photo", owner=user)
        photo_1 = baker.make("gallery.Photo")
        bookmark = Bookmark.objects.create(owner=user, photo=photo_1)
        serializer = BookmarkSerializer(
            data={"id": bookmark.id, "user": user, "photo": photo_1.id}
        )
        assert not serializer.is_valid()
        assert serializer.errors
        serializer = BookmarkSerializer(
            data={"id": bookmark.id, "user": user, "photo": photo.id}
        )
        assert not serializer.is_valid()
        assert serializer.errors

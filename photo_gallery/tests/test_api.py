import pytest
import json
from model_bakery import baker

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from gallery.models import Album, Photo, Comment, Bookmark


User = get_user_model()
pytestmark = pytest.mark.django_db
client = Client()


class TestAlbum:
    def test_alums_list(self, create_user):
        baker.make("gallery.Album", _quantity=5)
        url = reverse("v1:albums")
        user = create_user(username="test")
        client.force_login(user=user)
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_alums_user_list(self, create_user):
        user = create_user(username="test")
        client.force_login(user=user)
        baker.make("gallery.Album", owner=user, _quantity=5)
        url = reverse("v1:user_albums", kwargs={"user_pk": user.id})
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_alums_list_superuser(self, create_user):
        baker.make("gallery.Album", _quantity=5)
        url = reverse("v1:albums")
        user = create_user(is_superuser=True)
        client.force_login(user=user)
        response = client.get(url)
        assert response.status_code == 403

    def test_album_retrieve(self, create_user):
        user = create_user(username="test")
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user)
        url = reverse("v1:album", kwargs={"pk": album.id})
        response = client.get(url)
        assert response.status_code == 200
        assert response.json() == {"id": album.id, "name": album.name}

    def test_album_create(self, create_user):
        url = reverse("v1:albums")
        user = create_user(username="test")
        client.force_login(user=user)
        expected_json = {"id": 1, "name": "album name"}
        response = client.post(
            url,
            {"name": "album name", "owner_id": user.id},
            content_type="application/json",
        )
        assert response.status_code == 201
        assert json.loads(response.content) == expected_json
        assert Album.objects.all().count() == 1

    def test_album_delete(self, create_user):
        user = create_user(username="test")
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user)
        baker.make("gallery.Photo", owner=user, album=album, _quantity=5)
        assert Album.objects.all().count() == 1
        assert Photo.objects.all().count() == 5
        url = reverse("v1:album", kwargs={"pk": album.id})
        response = client.delete(url)
        assert response.status_code == 204
        assert Album.objects.all().count() == 0
        assert Photo.objects.all().count() == 0

    def test_album_update(self, create_user):
        user = create_user()
        client.force_login(user=user)
        old_album = Album.objects.create(owner=user, name="album name")
        assert Album.objects.all().count() == 1
        album_dict = {"id": old_album.id, "name": "new album name"}
        url = reverse("v1:album", kwargs={"pk": old_album.id})
        response = client.put(
            url, data=album_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 200
        assert json.loads(response.content) == album_dict
        assert Album.objects.all().count() == 1


class TestPhoto:
    def test_photos_list(self, create_user):
        baker.make("gallery.Photo", _quantity=5)
        url = reverse("v1:photos")
        user = create_user(username="test")
        client.force_login(user=user)
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5

    def test_photo_partial_update(self, create_user):
        user = create_user()
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user)
        old_photo = baker.make("gallery.Photo", owner=user, album=album)
        assert Photo.objects.all().count() == 1
        photo_dict = {"id": old_photo.id, "description": "new description"}
        url = reverse("v1:photo", kwargs={"pk": old_photo.id})
        response = client.patch(
            url, data=photo_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 200
        assert json.loads(response.content)["description"] == "new description"
        assert Photo.objects.all().count() == 1

    def test_photo_update_error(self, create_user):
        user = create_user()
        client.force_login(user=user)
        old_photo = baker.make("gallery.Photo")
        assert Photo.objects.all().count() == 1
        photo_dict = {"id": old_photo.id, "description": "new description"}
        url = reverse("v1:photo", kwargs={"pk": old_photo.id})
        response = client.patch(
            url, data=photo_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 400
        assert Photo.objects.all().count() == 1

    def test_photo_delete_error(self, create_user):
        user = create_user(username="test")
        client.force_login(user=user)
        photo = baker.make("gallery.Photo")
        assert Photo.objects.all().count() == 1
        url = reverse("v1:photo", kwargs={"pk": photo.id})
        response = client.delete(url)
        assert response.status_code == 403
        assert Photo.objects.all().count() == 1


class TestComment:
    def test_comment_list(self, create_user, create_user_1):
        user = create_user(username="test")
        user_1 = create_user_1(username="test_1")
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user_1)
        photo = baker.make("gallery.Photo", owner=user_1, album=album)
        baker.make("gallery.Comment", owner=user, photo=photo)
        url = reverse("v1:photo_comments", kwargs={"photo_pk": photo.id})
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1

    def test_comment_create(self, create_user, create_user_1):
        user = create_user(username="test")
        user_1 = create_user_1(username="test_1")
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user_1)
        photo = baker.make("gallery.Photo", owner=user_1, album=album)
        url = reverse("v1:photo_comments", kwargs={"photo_pk": photo.id})
        response = client.post(
            url,
            {"photo": photo.id, "text": "comment", "owner": user.id},
            content_type="application/json",
        )
        assert response.status_code == 201
        assert json.loads(response.content)["text"] == "comment"
        assert Comment.objects.all().count() == 1

    def test_comment_delete(self, create_user, create_user_1):
        user = create_user(username="test")
        user_1 = create_user_1(username="test_1")
        client.force_login(user=user)
        album = baker.make("gallery.Album", owner=user_1)
        photo = baker.make("gallery.Photo", owner=user_1, album=album)
        comment = baker.make("gallery.Comment", owner=user, photo=photo)
        assert Comment.objects.all().count() == 1
        url = reverse("v1:comment_delete", kwargs={"pk": comment.id})
        response = client.delete(url)
        assert response.status_code == 204
        assert Comment.objects.all().count() == 0


class TestBookmark:
    def test_bookmark_list(self, create_user):
        user = create_user()
        client.force_login(user=user)
        baker.make("gallery.Bookmark", _quantity=5)
        url = reverse("v1:bookmarks")
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5
        assert Bookmark.objects.all().count() == 5

    def test_bookmark_user_list(self, create_user):
        user = create_user()
        client.force_login(user=user)
        baker.make("gallery.Bookmark", owner=user, _quantity=5)
        url = reverse("v1:user_bookmarks", kwargs={"user_pk": user.id})
        response = client.get(url)
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 5
        assert Bookmark.objects.all().count() == 5

    def test_bookmark_user_list_not_found(self, create_user):
        user = create_user()
        client.force_login(user=user)
        url = reverse("v1:user_bookmarks", kwargs={"user_pk": user.id})
        response = client.get(url)
        assert response.status_code == 404

    def test_bookmark_not_user_list(self):
        baker.make("gallery.Bookmark", _quantity=5)
        url = reverse("v1:bookmarks")
        response = client.get(url)
        assert response.status_code == 401


class TestFeed:
    def test_list(self, create_user):
        user = create_user()
        client.force_login(user=user)
        photo = baker.make("gallery.Photo")
        photo_1 = baker.make("gallery.Photo")
        baker.make("gallery.Bookmark", photo=photo, _quantity=3)
        baker.make("gallery.Bookmark", photo=photo_1, _quantity=1)
        baker.make("gallery.Comment", photo=photo)
        baker.make("gallery.Comment", photo=photo_1, _quantity=6)
        url = reverse("v1:feed")
        response = client.get(url)
        assert response.status_code == 200
        assert json.loads(response.content)[0]["id"] == photo_1.id

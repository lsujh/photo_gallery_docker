import pytest

from django.db.models.signals import post_delete
from django.test import Client

from model_bakery import baker

from gallery.models import Photo

pytestmark = pytest.mark.django_db
client = Client()


class TestModels:
    def test_album(self):
        album = baker.make("gallery.Album")
        assert album.__str__() == album.name

    def test_photo(self):
        photo = baker.make("gallery.Photo")
        assert photo.__str__() == f"{photo.album.name} {str(photo.id)}"

    def test_comment(self):
        comment = baker.make("gallery.Comment")
        assert comment.__str__() == f"{comment.owner.username} {str(comment.photo)}"

    def test_bookmark(self):
        bookmark = baker.make("gallery.Bookmark")
        assert (
            bookmark.__str__() == f"{bookmark.owner.username} {str(bookmark.photo.id)}"
        )

    def test_post_delete(self, create_user):
        user = create_user()
        client.force_login(user=user)
        photo = baker.make('gallery.Photo')
        result = post_delete.send(Photo, instance=photo)
        assert result

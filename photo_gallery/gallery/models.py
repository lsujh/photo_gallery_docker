from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver

User = get_user_model()


class Album(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Photo(models.Model):
    description = models.TextField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="")

    def __str__(self):
        return f"{self.album.name} {self.id}"


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.username} {str(self.photo)}"


class Bookmark(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.username} {str(self.photo.id)}"


@receiver(post_delete, sender=Photo)
def delete_associated_files(sender, instance, **kwargs):
    path = instance.photo.name
    if path:
        default_storage.delete(path)

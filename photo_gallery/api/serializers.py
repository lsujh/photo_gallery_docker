from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation as validators

from rest_framework import serializers

from gallery.models import Album, Photo, Comment, Bookmark

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "first_name", "last_name")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user = User(**data)
        password = data.get("password")
        validators.validate_password(password=password, user=user)
        return super(SignupSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = (
            "id",
            "name",
        )

    def validate(self, attrs):
        attrs["owner"] = self.initial_data["user"]
        pk = self.initial_data.get("id")
        if pk:
            attrs["id"] = pk
            if not Album.objects.filter(owner=attrs["owner"], id=pk):
                raise serializers.ValidationError("You cannot update this album.")
        return attrs


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "id",
            "description",
            "album",
            "photo",
        )

    def validate(self, attrs):
        attrs["owner"] = self.initial_data["user"]
        pk = self.initial_data.get("id")
        if pk:
            attrs["id"] = pk
            if not Photo.objects.filter(owner=attrs["owner"], id=pk):
                raise serializers.ValidationError("You cannot update this photo.")
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "photo",
            "text",
        )

    def validate(self, attrs):
        attrs["owner"] = self.initial_data["user"]
        if Comment.objects.filter(owner=attrs["owner"], photo=attrs["photo"]):
            raise serializers.ValidationError(
                "You have already commented on this photo."
            )
        elif Photo.objects.filter(owner=attrs["owner"]):
            raise serializers.ValidationError("You cannot commented your photo.")
        return attrs


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = (
            "id",
            "photo",
        )

    def validate(self, attrs):
        attrs["owner"] = self.initial_data["user"]
        if Photo.objects.filter(owner=attrs["owner"], id=attrs["photo"].id):
            raise serializers.ValidationError("You cannot favorite your photo.")
        elif Bookmark.objects.filter(owner=attrs["owner"], photo=attrs["photo"]):
            raise serializers.ValidationError(
                "You have already added this photo to your favorites."
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")

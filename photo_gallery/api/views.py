from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from gallery.models import Album, Photo, Comment, Bookmark
from .serializers import (
    SignupSerializer,
    AlbumSerializer,
    PhotoSerializer,
    CommentSerializer,
    BookmarkSerializer,
    UserSerializer,
)

from .permissions import IsNotSuperUser


User = get_user_model()


class CreateMixin:
    lookup_field = "pk"
    lookup_url_kwarg = "id"

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


class ListUserMixin:
    def list(self, request, *args, **kwargs):
        user_id = self.kwargs.get("user_pk")
        queryset = self.queryset.filter(owner_id=user_id)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=404)


class DestroyMixin:
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        user_id = request.user.id
        if self.queryset.filter(owner_id=user_id, id=pk):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=204)
        else:
            return Response(status=403)


class UpdateMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data
        data["user"] = request.user
        data["id"] = kwargs.get("pk")
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class SignupApi(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return Response(serializer.data, status=201)


class AlbumApi(CreateMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class AlbumRetrieveUpdateDestroyApi(UpdateMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class PhotoApi(CreateMixin, ListCreateAPIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class PhotoRetrieveUpdateDestroyApi(
    UpdateMixin, DestroyMixin, RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class UserAlbumsApi(ListUserMixin, ListAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class UserPhotosApi(ListUserMixin, ListAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()


class CommentApi(CreateMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, *args, **kwargs):
        photo_id = self.kwargs["photo_pk"]
        queryset = Comment.objects.filter(photo_id=photo_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentDeleteApi(DestroyMixin, DestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class BookmarkApi(CreateMixin, CreateAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


class BookmarksListApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


class UserBookmarksApi(ListUserMixin, ListAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


class BookmarkDeleteApi(DestroyMixin, DestroyAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()


class FeedApi(ListAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = (
            self.queryset.annotate(cnt=Count("comment") + Count("bookmark"))
            .order_by("-cnt")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserApi(GenericAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        queryset = self.queryset.filter(id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UserIdApi(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsNotSuperUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

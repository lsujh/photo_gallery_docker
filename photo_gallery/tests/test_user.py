import json

import pytest

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from api.serializers import SignupSerializer

User = get_user_model()
pytestmark = pytest.mark.django_db
client = Client()


class TestUser:
    def test_register(self, client):
        assert User.objects.all().count() == 1
        data = {
            "username": "user",
            "password": "password001",
            "email": "test@email.com",
        }
        res = client.post("/api/signup/", data=data, content_type="application/json")
        assert res.status_code == 201
        assert User.objects.all().count() == 2

    def test_register_fail_no_password(self):
        assert User.objects.all().count() == 1
        data = {"username": "user", "email": "test@email.com"}
        res = client.post("/api/signup/", data=data, content_type="application/json")
        assert res.status_code == 400
        assert User.objects.all().count() == 1

    def test_register_fail_no_username(self):
        assert User.objects.all().count() == 1
        data = {"password": "password001", "email": "test@email.com"}
        res = client.post("/api/signup/", data=data, content_type="application/json")
        assert res.status_code == 400
        assert User.objects.all().count() == 1

    def test_user_detail(self, create_user):
        res = client.get("/api/user/1/")
        assert res.status_code == 401
        user = create_user()
        client.force_login(user=user)
        res = client.get(reverse("v1:user_id", kwargs={"pk": user.id}))
        assert res.status_code == 200

    def test_not_user_detail(self):
        res = client.get("/api/user/2/")
        assert res.status_code == 401

    def test_user_me_detail(self, create_user):
        user = create_user()
        client.force_login(user=user)
        res = client.get(f"/api/user/me/")
        assert res.status_code == 200

    def test_user_model(self, create_user):
        user = create_user()
        assert user.__str__() == user.email

    def test_serialize_data(self):
        data = {
            "id": 1,
            "username": "username",
            "email": "user@email.com",
            "password": "user1password",
        }
        serializer = SignupSerializer(data=data)
        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}

    def test_serialize_data_error(self):
        data = {
            "id": 1,
            "username": "username",
            "email": "user@email.com",
            "password": "user",
        }
        serializer = SignupSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors

    def test_user_update(self, create_user):
        user = create_user()
        client.force_login(user=user)
        assert User.objects.all().count() == 2
        user_dict = {
            "id": user.id,
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": user.email,
            "username": user.username,
        }
        url = reverse("v1:user")
        response = client.put(
            url, data=user_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 200
        assert json.loads(response.content) == user_dict
        assert User.objects.all().count() == 2

    def test_user_update_error(self, create_user):
        user = create_user()
        client.force_login(user=user)
        assert User.objects.all().count() == 2
        user_dict = {"id": user.id, "last_name": "Ivanov", "username": user.username}
        url = reverse("v1:user")
        response = client.put(
            url, data=user_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 400
        assert User.objects.all().count() == 2

    def test_user_partial_update(self, create_user):
        user = create_user()
        client.force_login(user=user)
        assert User.objects.all().count() == 2
        user_dict = {
            "id": user.id,
            "last_name": "Ivanov",
            "email": user.email,
            "username": user.username,
        }
        url = reverse("v1:user")
        response = client.patch(
            url, data=user_dict, content_type="application/json", follow=True
        )
        assert response.status_code == 200
        assert json.loads(response.content)["last_name"] == "Ivanov"
        assert User.objects.all().count() == 2

import pytest


@pytest.fixture
def test_password():
    return "password"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["email"] = "test@test.ua"
        kwargs["password"] = test_password
        kwargs["username"] = "test"
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def create_user_1(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["email"] = "test@example.com"
        kwargs["password"] = test_password
        kwargs["username"] = "test_1"
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user(username="test")
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login

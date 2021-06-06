from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email_confirm = models.BooleanField(default=True)
    email = models.EmailField(
        validators=[validators.validate_email], max_length=255, unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email

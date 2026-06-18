from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from dershop.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        is_active=True,
        is_admin=False,
        password=None,
    ):
        if not email or not first_name or not last_name:
            raise ValueError("User email, first_name, and last_name is cannot empty")

        user = self.model(
            email=self.normalize_email(email.lower()),
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not extra_fields.get("first_name"):
            raise ValueError("Superuser first name should not empty")
        if not extra_fields.get("last_name"):
            raise ValueError("Superuser last name should not empty.")

        first_name = extra_fields.get("first_name")
        last_name = extra_fields.get("last_name")

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin

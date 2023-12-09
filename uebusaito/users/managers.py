from typing import Any

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager

from uebusaito.users.models import User


class UserCreationError(ValueError):
    def __init__(self, reason: str) -> None:
        super().__init__(f"Error when creating a user: {reason}")


class UserManager(DjangoUserManager):
    """Custom manager for the User model."""

    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields: Any,  # noqa: ANN401
    ) -> User:
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise UserCreationError(reason="The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401
    ) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,  # noqa: ANN401
    ) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise UserCreationError(reason="Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise UserCreationError(reason="Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

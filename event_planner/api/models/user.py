from typing import Any, ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models as m


class CustomUserManager(UserManager["User"]):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields: Any) -> "User":
        """Create and save a user with the given email, and password."""
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user: User = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(  # type: ignore[override]
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        """Create and save a normal user."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(  # type: ignore[override]
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> "User":
        """Create and save superuser."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects: ClassVar[CustomUserManager] = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    email = m.EmailField(unique=True, blank=False, null=False)

    # The username field is inherited from AbstractUser, but we don't want to use it.
    # Therefore we remove it as described in the docs. [0]
    # Unfortunately, this means that we need to disable type checking for this field,
    # as django-stubs defines it as a simple CharField. [1]
    #
    # See more:
    # [0] https://docs.djangoproject.com/en/dev/topics/db/models/#field-name-hiding-is-not-permitted
    # [1] https://github.com/typeddjango/django-stubs/issues/433
    username = None  # type: ignore[assignment]

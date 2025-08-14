# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    Custom User model inheriting from Django's AbstractUser and our BaseModel.
    `id` from BaseModel will override the default integer ID.
    Username, email, first_name, and last_name are inherited from AbstractUser.
    """

    # Override default username validation and help text if needed
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)

    # We don't need first_name/last_name if a full name field is preferred
    # name = models.CharField(_("Full Name"), blank=True, max_length=255)

    # Let's use email as the primary identifier for login
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

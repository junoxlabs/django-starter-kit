# apps/core/models.py

import uuid
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Custom manager to exclude soft-deleted objects from default querysets.
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    """
    An abstract base model with common fields.
    - id: UUID primary key.
    - created_at: Timestamp when the object was created.
    - updated_at: Timestamp when the object was last updated.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteModel(BaseModel):
    """
    An abstract base model that provides soft delete functionality.
    Inherits from BaseModel.
    """

    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    # Managers
    objects = SoftDeleteManager()  # Default manager, filters out deleted items.
    all_objects = models.Manager()  # Manager to access all items, including deleted.

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marks the instance as deleted."""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restores a soft-deleted instance."""
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        """Returns True if the instance is soft-deleted."""
        return self.deleted_at is not None

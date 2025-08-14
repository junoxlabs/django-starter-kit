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


class SearchManager(models.Manager):
    """
    Custom manager for ParadeDB BM25 search functionality.
    """
    
    def search(self, query, fields=None):
        """
        Perform a BM25 search on specified fields.
        :param query: The search query string
        :param fields: List of fields to search in
        :return: QuerySet with search results
        """
        if fields is None:
            fields = ['description']
            
        # Construct the search clause using ParadeDB's @@@ operator
        search_clauses = []
        for field in fields:
            search_clauses.append(f"{field} @@@ %s")
            
        search_condition = " OR ".join(search_clauses)
        return self.extra(where=[search_condition], params=[query] * len(fields))
    
    def scored_search(self, query, fields=None):
        """
        Perform a scored BM25 search using paradedb.score().
        :param query: The search query string
        :param fields: List of fields to search in
        :return: QuerySet with search results including scores
        """
        if fields is None:
            fields = ['description']
            
        # Construct the search clause using ParadeDB's @@@ operator
        search_clauses = []
        for field in fields:
            search_clauses.append(f"{field} @@@ %s")
            
        search_condition = " OR ".join(search_clauses)
        score_select = "paradedb.score({}) as search_score".format(
            self.model._meta.pk.column
        )
        
        return self.extra(
            where=[search_condition],
            params=[query] * len(fields),
            select={'search_score': score_select}
        ).order_by('-search_score')


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

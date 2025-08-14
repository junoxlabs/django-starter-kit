# apps/core/search.py
from django.db import models

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
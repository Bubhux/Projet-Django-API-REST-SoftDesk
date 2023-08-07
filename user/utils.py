from django.db import models

from api.models import Contributor


contributed_projects_count = models.PositiveIntegerField(default=0)

def contributed_projects_count(self):
    """Retourne le nombre de projets auxquels l'utilisateur a contribué"""
    return self.contributor_set.values('project').distinct().count()
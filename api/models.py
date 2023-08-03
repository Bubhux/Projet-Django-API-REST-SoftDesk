from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


# Types de projet possibles
TYPES = [('BACKEND', 'BACKEND'), ('FRONTEND', 'FRONTEND'), ('iOS', 'iOS'), ('ANDROID', 'ANDROID')]

# Rôles possibles des utilisateurs dans un projet
ROLES = [('AUTHOR', 'AUTHOR'), ('CONTRIBUTOR', 'CONTRIBUTOR')]

# Tags possibles pour les problèmes (issues)
TAGS = [('BUG', 'BUG'), ('TASK', 'TASK'), ('UPGRADE', 'UPGRADE')]

# Priorités possibles pour les problèmes (issues)
PRIORITIES = [('LOW', 'LOW'), ('MEDIUM', 'MEDIUM'), ('HIGH', 'HIGH')]

# Statuts possibles pour les problèmes (issues)
STATUSES = [('TODO', 'TODO'), ('IN PROGRESS', 'IN PROGRESS'), ('DONE', 'DONE')]


class Project(models.Model):
    """Classe représentant un projet"""

    # Champs du projet
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=2048)
    type_development = models.CharField(choices=TYPES, max_length=12)
    # Relation avec l'auteur du projet (un utilisateur)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.title


class Contributor(models.Model):
    """Classe représentant un contributeur à un projet"""

    # Relation avec l'utilisateur (contributeur)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Relation avec le projet auquel le contributeur participe
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    # Rôle du contributeur dans le projet (parmi les choix définis dans la liste ROLES)
    role = models.CharField(choices=ROLES, max_length=11, default='CONTRIBUTOR')
    # Définition d'une contrainte d'unicité pour que le même contributeur ne puisse pas être associé au même projet plusieurs fois
    class Meta:
        """Définition d'une contrainte d'unicité pour que le même contributeur ne puisse pas être associé au même projet plusieurs fois"""
        unique_together = ('project_id', 'user_id')

    def __str__(self):
        return self.user.username


class Issue(models.Model):
    """Classe représentant un problème (issue) lié à un projet"""

    # Champs du problème
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)

    # Relation avec l'auteur du problème (un utilisateur)
    priority = models.CharField(choices=PRIORITIES, max_length=12, default='LOW')
    tag = models.CharField(choices=TAGS, max_length=12)
    status = models.CharField(choices=STATUSES, max_length=11, default='TODO')

    # Relation avec l'auteur du problème (un utilisateur)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issue_author')

    # Relation avec l'utilisateur assigné au problème (un contributeur)
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE, related_name='issue_assignee')

    # Relation avec le projet auquel le problème est lié
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='issues')

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Classe représentant un commentaire lié à un problème (issue)"""

    description = models.CharField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)

    # Relation avec l'auteur du commentaire (un utilisateur)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_author')
    # Relation avec le problème auquel le commentaire est lié
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.author.username

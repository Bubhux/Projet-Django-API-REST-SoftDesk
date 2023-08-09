from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from api.models import Project, Issue, Comment


class ProjectPermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API gérant les opérations CRUD sur les objets Project.

    Cette classe permet de contrôler l'accès aux opérations CRUD sur les objets Project
    en fonction de l'utilisateur connecté et de son rôle (contributeur ou auteur du projet).

    Méthode has_permission:
        - Récupère le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        - Si 'project_pk' n'est pas spécifié dans l'URL, l'accès est autorisé sans restriction de permission.
        - Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès aux contributeurs du projet.
        - Pour les autres méthodes (POST, PUT, DELETE), vérifie si l'utilisateur connecté est l'auteur du projet.
    """
    def has_permission(self, request, view):
        # Récupère le projet spécifié par la clé primaire 'project_pk' dans l'URL
        try:
            project = get_object_or_404(Project, id=view.kwargs['project_pk'])
            # Vérifie si la méthode de requête est une méthode sécurisée (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                # Autorise l'accès aux méthodes sécurisées pour les contributeurs du projet
                # Vérifie si l'utilisateur connecté est l'auteur du projet pour les autres méthodes (POST, PUT, DELETE)
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == project.author
        except KeyError:
            # Si 'project_pk' n'est pas spécifié dans l'URL, l'accès est autorisé (aucune restriction de permission)
            return True


class ContributorPermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API gérant les contributeurs d'un objet Project spécifique.

    Cette classe permet de contrôler l'accès aux opérations CRUD sur les contributeurs
    d'un objet Project en fonction de l'utilisateur connecté et de son rôle (contributeur ou auteur du projet).

    Méthode has_permission:
        - Récupère le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        - Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès aux contributeurs du projet.
        - Pour les autres méthodes (POST, PUT, DELETE), vérifie si l'utilisateur connecté est l'auteur du projet.
    """
    def has_permission(self, request, view):
        try:
            # Récupérer le projet spécifié par la clé primaire 'project_pk' dans l'URL.
            project = get_object_or_404(Project, id=view.kwargs['project_pk'])

            if request.method in permissions.SAFE_METHODS:
                # Pour les méthodes sécurisées (GET, HEAD, OPTIONS), autorise l'accès aux contributeurs du projet.
                return project in Project.objects.filter(contributors__user=request.user)
            else:
                # Pour les autres méthodes (POST, PUT, DELETE),
                # vérifie si l'utilisateur connecté est l'auteur du projet.
                return request.user == project.author
        except KeyError:
            # Si la clé 'project_pk' n'est pas trouvée dans le dictionnaire view.kwargs,
            # renvoyer False pour refuser l'accès.
            return False


class IssuePermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API gérant les issues d'un objet Project spécifique.

    Cette classe permet de contrôler l'accès aux opérations CRUD sur les issues d'un objet Project
    en fonction de l'utilisateur connecté et de son rôle (auteur de l'issue).

    Méthode has_permission:
        - Récupère le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        - Vérifie si l'utilisateur connecté est l'auteur de l'issue
          (pour les méthodes sécurisées - GET, HEAD, OPTIONS).
        - Vérifie si l'utilisateur connecté est un contributeur du projet
          (pour les autres méthodes - POST, PUT, DELETE).
    """

    def has_permission(self, request, view):
        # Récupérer le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])

        if request.method in permissions.SAFE_METHODS:
            try:
                # Pour les méthodes sécurisées (GET, HEAD, OPTIONS),
                # vérifie si l'utilisateur connecté est l'auteur de l'issue.
                issue = get_object_or_404(Issue, id=view.kwargs['issue_pk'])
                return request.user == issue.author
            except KeyError:
                # Pour les méthodes sécurisées (GET, HEAD, OPTIONS) sans spécification de l'issue,
                # on vérifie si l'utilisateur connecté est un contributeur du projet.
                return project in Project.objects.filter(contributors__user=request.user)
        else:
            # Pour les autres méthodes (POST, PUT, DELETE),
            # on vérifie si l'utilisateur connecté est un contributeur du projet.
            return project in Project.objects.filter(contributors__user=request.user)


class CommentPermissions(permissions.BasePermission):
    """
    Classe de permission personnalisée pour la vue de l'API
    gérant les commentaires d'un issue spécifique d'un objet Project.

    Cette classe permet de contrôler l'accès aux opérations CRUD sur les commentaires d'un issue d'un objet Project
    en fonction de l'utilisateur connecté et de son rôle (auteur du commentaire).

    Méthode has_permission:
        - Récupère le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        - Vérifie si l'utilisateur connecté est l'auteur du commentaire
          (pour les méthodes sécurisées - GET, HEAD, OPTIONS).
        - Vérifie si l'utilisateur connecté est un contributeur du projet
          (pour les autres méthodes - POST, PUT, DELETE).
    """
    def has_permission(self, request, view):
        # Récupérer le projet spécifié par la clé primaire 'project_pk' dans l'URL.
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])

        if request.method in permissions.SAFE_METHODS:
            try:
                # Étape 2 : Pour les méthodes sécurisées (GET, HEAD, OPTIONS),
                # vérifie si l'utilisateur connecté est l'auteur du commentaire.
                comment = get_object_or_404(Comment, id=view.kwargs['comment_pk'])
                return request.user == comment.author
            except KeyError:
                # Étape 3 : Pour les méthodes sécurisées (GET, HEAD, OPTIONS) sans spécification du commentaire,
                # on vérifie si l'utilisateur connecté est un contributeur du projet.
                return project in Project.objects.filter(contributors__user=request.user)
        else:
            # Étape 4 : Pour les autres méthodes (POST, PUT, DELETE),
            # on vérifie si l'utilisateur connecté est un contributeur du projet.
            return project in Project.objects.filter(contributors__user=request.user)

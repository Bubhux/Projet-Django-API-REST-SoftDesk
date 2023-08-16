from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

from api.models import Project, Issue, Contributor, Comment
from api.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
from api.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ContributorListSerializer,
    ContributorDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentListSerializer,
    CommentDetailSerializer
)
from user.serializers import UserSignupSerializer
from user.models import User


class MultipleSerializerMixin:
    """Mixin pour utiliser plusieurs classes de sérialiseur dans une vue."""

    # Par défaut, la variable detail_serializer_class est définie sur None.
    # Ce qui signifie qu'il n'y a pas de sérialiseur spécifique défini pour les actions de type
    # "retrieve", "create", "update" et "destroy".
    detail_serializer_class = None

    def get_serializer_class(self):
        if (self.action == 'retrieve' or
                self.action == 'create' or
                self.action == 'update' or
                self.action == 'destroy') and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class AdminUserViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet personnalisée pour les utilisateurs administrateurs.
    """
    serializer_class = UserSignupSerializer

    def get_queryset(self):
        return User.objects.all()


class AdminProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet personnalisée pour les projets administrateurs.
    """
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()


class AdminUserContibutorViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet personnalisée pour les contributeurs d'utilisateurs administrateurs.
    """
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class AdminIssueViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet personnalisée pour les problèmes administrateurs.
    """
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()


class AdminCommentViewSet(MultipleSerializerMixin, ModelViewSet):
    """
    ViewSet personnalisée pour les commentaires administrateurs.
    """
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les opérations CRUD sur les objets Project."""

    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def perform_create(self, serializer):
        """Sauvegarde l'objet Project avec l'utilisateur actuellement connecté en tant qu'auteur."""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET'])
    def user_projects(self, request):
        """Renvoie tous les projets où l'utilisateur est à la fois l'auteur et le contributeur."""
        user = self.request.user
        projects = Project.objects.filter(author=user, contributors__user=user)
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        """Met à jour l'objet Project spécifié par la clé primaire passée dans l'URL."""
        project = self.get_object()
        data = request.data.copy()
        data['author'] = project.author.id
        serializer = ProjectListSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk=None, pk=None):
        """Supprime l'objet Project spécifié par la clé primaire passée dans l'URL."""
        project = self.get_object()

        # Utilise la permission pour vérifier si l'utilisateur est l'auteur du projet
        if not self.request.user == project.author:
            return Response("You don't have permission to delete this project.", status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response('Project successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class UserContributorsViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les contributeurs d'un objet Project spécifique."""

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_project(self, project_pk):
        """Récupère l'objet Project spécifié par la clé primaire passée dans l'URL."""
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self):
        """Renvoie les contributeurs associés à l'objet Project spécifié dans l'URL."""
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        return Contributor.objects.filter(project=project)

    def create(self, request, project_pk):
        """Ajoute un nouveau contributeur à l'objet Project spécifié dans l'URL."""
        project = self.get_project(project_pk)
        data = request.data.copy()
        data['project'] = project.id

        try:
            Contributor.objects.get(user=data['user'], project=project.id)
            return Response('This user has already been added.', status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response('This user does not exist.', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, project_pk, pk):
        """Supprime le contributeur spécifié de l'objet Project spécifié."""
        contributor = self.get_object()
        if contributor.role == 'AUTHOR':
            return Response('Project author cannot be deleted.', status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les issues d'un objet Project spécifique."""

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IssuePermissions]

    def get_project(self, project_pk):
        """Récupère l'objet Project spécifié par la clé primaire passée dans l'URL."""
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self):
        """Renvoie les issues associées à l'objet Project spécifié dans l'URL."""
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        """Sauvegarde un nouvel objet Issue associé à l'objet Project spécifié et à l'auteur actuellement connecté."""
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        assignee_id = self.request.data.get('assignee')
        print(f"Assignee ID from request data: {assignee_id}")
        if assignee_id:
            try:
                assignee = get_user_model().objects.get(id=assignee_id)
                serializer.save(project=project, author=self.request.user, assignee=assignee)
                print(f"Assignee found: {assignee}")
            except get_user_model().DoesNotExist:
                print("Assignee not found")
                try:
                    assignee = get_user_model().objects.get(id=assignee_id)
                except get_user_model().DoesNotExist:
                    raise serializers.ValidationError("Invalid assignee ID")
        else:
            serializer.save(project=project, author=self.request.user)

    def update(self, request, project_pk, pk):
        """Met à jour l'objet Issue spécifié associé à l'objet Project spécifié."""
        issue = self.get_object()
        serializer = self.serializer_class(issue, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def create(self, request, project_pk):
        """Crée un nouvel objet Issue associé à l'objet Project spécifié."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, project_pk, pk):
        """Supprime l'objet Issue spécifié associé à l'objet Project spécifié."""
        issue = self.get_object()
        issue.delete()
        return Response('Issue successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'API pour gérer les commentaires d'un issue spécifique d'un objet Project."""

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_project_and_issue(self, project_pk, issue_pk):
        """Récupère l'objet Project et l'objet Issue spécifiés par les clés primaires passées dans l'URL."""
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        return project, issue

    def get_queryset(self):
        """Renvoie les commentaires associés à l'objet Issue spécifié dans l'URL."""
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        """Sauvegarde un nouveau commentaire associé à l'objet Issue spécifié et à l'auteur actuellement connecté."""
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        serializer.save(issue=issue, author=self.request.user)

    def perform_update(self, serializer):
        """Met à jour l'objet Comment avec les nouvelles données en conservant l'issue et l'auteur d'origine."""
        comment = self.get_object()
        serializer.save(issue=comment.issue, author=comment.author)

    def perform_destroy(self, instance):
        """Supprime l'objet Comment spécifié."""
        instance.delete()

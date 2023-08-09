from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth import get_user_model

from api.models import Comment, Contributor, Issue, Project


User = get_user_model()


class ProjectListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher une liste d'objets Project.

    Ce sérialiseur est utilisé pour représenter une liste d'objets Project
    lorsqu'ils sont récupérés via une requête GET sur l'endpoint 'api/projects/'.
    Il inclut uniquement les champs 'author' et 'id' dans la réponse, qui seront en lecture seule.
    """
    class Meta:
        model = Project
        fields = ['author', 'id', 'title', 'description']


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les détails d'un objet Project.

    Ce sérialiseur est utilisé pour représenter les détails d'un objet Project
    lorsqu'il est récupéré via une requête GET sur l'endpoint 'api/projects/<pk>/'.
    Il inclut les champs 'author', 'id', 'title', 'description', 'type' et 'issues' dans la réponse.
    Le champ 'issues' est un SerializerMethodField qui permet d'inclure les détails des objets Issue associés.
    """
    issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['author', 'id', 'title', 'description', 'type_development', 'issues']

    def get_issues(self, instance):
        """Obtient les détails des objets Issue associés à l'objet Project.

        Cette méthode est utilisée pour obtenir les détails des objets Issue associés à l'objet Project
        et les inclure dans la réponse. Elle utilise un queryset pour filtrer les objets Issue
        qui sont liés à l'objet Project spécifié par 'instance.id'.

        Args:
            instance: Instance de l'objet Project pour lequel on souhaite obtenir les issues associés.

        Returns:
            Une liste de dictionnaires représentant les détails des objets Issue associés.
        """
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data


class ContributorListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher une liste d'objets Contributor.

    Ce sérialiseur est utilisé pour représenter une liste d'objets Contributor
    lorsqu'ils sont récupérés via une requête GET sur l'endpoint 'api/users/'.
    Il inclut uniquement les champs 'user' et 'project' dans la réponse, qui seront en lecture seule.
    """
    class Meta:
        model = Contributor
        fields = ['user', 'project', 'id', 'role']


class ContributorDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les détails d'un objet Contributor.

    Ce sérialiseur est utilisé pour représenter les détails d'un objet Contributor
    lorsqu'il est récupéré via une requête GET sur l'endpoint 'api/users/<pk>/'.
    Il inclut les champs 'user', 'project', 'role', 'id' et 'projects' dans la réponse.
    Le champ 'projects' est un SerializerMethodField qui permet d'inclure les détails des objets Project associés.
    """
    projects = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'role', 'id', 'projects']

    def get_projects(self, instance):
        """Obtient les détails des objets Project associés à l'objet Contributor.

        Cette méthode est utilisée pour obtenir les détails des objets Project associés à l'objet Contributor
        et les inclure dans la réponse. Elle utilise un queryset pour filtrer les objets Project
        qui sont liés à l'objet Contributor spécifié par 'instance.id'.

        Args:
            instance: Instance de l'objet Contributor pour lequel on souhaite obtenir les projets associés.

        Returns:
            Une liste de dictionnaires représentant les détails des objets Project associés.
        """
        queryset = Project.objects.filter(contributors__id=instance.id)
        return ProjectListSerializer(queryset, many=True).data


class IssueListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher une liste d'objets Issue.

    Ce sérialiseur est utilisé pour représenter une liste d'objets Issue
    lorsqu'ils sont récupérés via une requête GET sur l'endpoint 'api/issues/'.
    Il inclut les champs 'title', 'created_time', 'author' et 'id' dans la réponse,
    qui seront en lecture seule.
    """
    assignee_id = serializers.PrimaryKeyRelatedField(
        source='assignee.user',
        queryset=User.objects.all(),
        required=False, allow_null=True
    )

    class Meta:
        model = Issue
        fields = ['title', 'tag', 'created_time', 'author', 'id', 'description', 'assignee_id']


class IssueDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les détails d'un objet Issue.

    Ce sérialiseur est utilisé pour représenter les détails d'un objet Issue
    lorsqu'il est récupéré via une requête GET sur l'endpoint 'api/issues/<pk>/'.
    Il inclut les champs
    'title', 'description', 'created_time', 'priority', 'tag', 'status', 'author', 'id' et 'comments' dans la réponse.
    Le champ 'comments' est un SerializerMethodField qui permet d'inclure les détails des objets Comment associés.
    """
    comments = SerializerMethodField()
    assignee = serializers.PrimaryKeyRelatedField(queryset=Contributor.objects.all(), allow_null=False)

    class Meta:
        model = Issue
        fields = [
            'title',
            'description',
            'created_time',
            'priority',
            'tag',
            'status',
            'author',
            'id',
            'comments',
            'assignee'
        ]

    def get_comments(self, instance):
        """Obtient les détails des objets Comment associés à l'objet Issue.

        Cette méthode est utilisée pour obtenir les détails des objets Comment associés à l'objet Issue
        et les inclure dans la réponse. Elle utilise un queryset pour filtrer les objets Comment
        qui sont liés à l'objet Issue spécifié par 'instance.id'.

        Args:
            instance: Instance de l'objet Issue pour lequel on souhaite obtenir les commentaires associés.

        Returns:
            Une liste de dictionnaires représentant les détails des objets Comment associés.
        """
        queryset = Comment.objects.filter(issue_id=instance.id)
        return CommentListSerializer(queryset, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher une liste d'objets Comment.

    Ce sérialiseur est utilisé pour représenter une liste d'objets Comment
    lorsqu'ils sont récupérés via une requête GET sur l'endpoint 'api/comments/'.
    Il inclut les champs 'author' et 'id' dans la réponse, qui seront en lecture seule.
    """
    class Meta:
        model = Comment
        fields = ['author', 'id', 'description']


class CommentDetailSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les détails d'un objet Comment.

    Ce sérialiseur est utilisé pour représenter les détails d'un objet Comment
    lorsqu'il est récupéré via une requête GET sur l'endpoint 'api/comments/<pk>/'.
    Il inclut les champs 'author', 'description', 'created_time', 'issue', 'id' et 'issues' dans la réponse.
    Le champ 'issues' est un SerializerMethodField qui permet d'inclure les détails des objets Issue associés.
    """
    issues = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['author', 'description', 'created_time', 'issue', 'id', 'issues']

    def get_issues(self, instance):
        """Obtient les détails des objets Issue associés à l'objet Comment.

        Cette méthode est utilisée pour obtenir les détails des objets Issue associés à l'objet Comment
        et les inclure dans la réponse. Elle utilise un queryset pour filtrer les objets Issue
        qui sont liés à l'objet Comment spécifié par 'instance.id'.

        Args:
            instance: Instance de l'objet Comment pour lequel on souhaite obtenir les issues associés.

        Returns:
            Une liste de dictionnaires représentant les détails des objets Issue associés.
        """
        queryset = Issue.objects.filter(project_id=instance.id)
        return IssueListSerializer(queryset, many=True).data

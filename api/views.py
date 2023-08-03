from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets

from api.models import Project, Issue, Contributor, Comment
from api.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
from api.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from user.serializers import UserSignupSerializer


class ProjectListViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(contributors__user=self.request.user)


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def get_object(self):
        project_pk = self.kwargs.get('pk')
        return get_object_or_404(Project, id=project_pk)

    def put(self, request, pk=None):
        project = self.get_object()
        data = request.data.copy()
        data['author'] = project.author.id
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        project = self.get_object()
        project.delete()
        return Response('Project successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class UserContributorsListViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        return Contributor.objects.filter(project=project)

    def create(self, request, project_pk):
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


class UserContributorsDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_object(self):
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        contributor_pk = self.kwargs.get('contributor_pk')
        return get_object_or_404(Contributor, id=contributor_pk, project=project)

    def destroy(self, request, project_pk, contributor_pk):
        project = self.get_project(project_pk)
        contributor = self.get_object()
        if contributor.role == 'AUTHOR':
            return Response('Project author cannot be deleted.', status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class IssueListViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IssuePermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        return Issue.objects.filter(project=project)

    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')
        project = self.get_project(project_pk)
        serializer.save(project=project, author=self.request.user)

    def create(self, request, project_pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, project_pk, pk):
        project = self.get_project(project_pk)
        issue = self.get_object()
        issue.delete()
        return Response('Issue successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class IssueDetailViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IssuePermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_object(self):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        project = self.get_project(project_pk)
        return get_object_or_404(Issue, id=issue_pk, project=project)

    def perform_update(self, serializer):
        issue = self.get_object()
        serializer.save(project=issue.project, author=issue.author)

    def update(self, request, project_pk, issue_pk):
        issue = self.get_object()
        serializer = self.serializer_class(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, project_pk, issue_pk):
        issue = self.get_object()
        issue.delete()
        return Response('Issue successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class CommentListViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_project_and_issue(self, project_pk, issue_pk):
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        return project, issue

    def get_queryset(self):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        serializer.save(issue=issue, author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        serializer.save(issue=comment.issue, author=comment.author)

    def perform_destroy(self, instance):
        instance.delete()


class CommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_project_and_issue(self, project_pk, issue_pk):
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        return project, issue

    def get_object(self):
        project_pk = self.kwargs.get('project_pk')
        issue_pk = self.kwargs.get('issue_pk')
        comment_pk = self.kwargs.get('comment_pk')
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        return get_object_or_404(Comment, id=comment_pk, issue=issue)

    def perform_update(self, serializer):
        comment = self.get_object()
        serializer.save(issue=comment.issue, author=comment.author)

    def update(self, request, project_pk, issue_pk, comment_pk):
        comment = self.get_object()
        serializer = self.serializer_class(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, project_pk, issue_pk, comment_pk):
        comment = self.get_object()
        comment.delete()
        return Response('Comment successfully deleted.', status=status.HTTP_204_NO_CONTENT)

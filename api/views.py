from rest_framework import status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Project, Issue, Contributor, Comment
from api.permissions import ProjectPermissions, ContributorPermissions, IssuePermissions, CommentPermissions
from api.serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from rest_framework.views import APIView


class ProjectListViewSet(APIView):
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def get(self, request):
        projects = Project.objects.filter(contributors__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailViewSet(APIView):
    permission_classes = [IsAuthenticated, ProjectPermissions]

    def get_object(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get(self, request, project_pk):
        project = self.get_object(project_pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_pk):
        project = self.get_object(project_pk)
        data = request.data.copy()
        data['author'] = project.author.id
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_pk):
        project = self.get_object(project_pk)
        project.delete()
        return Response('Project successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class UserContributorsListViewSet(APIView):
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self, project):
        return Contributor.objects.filter(project=project)

    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        contributors = self.get_queryset(project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_pk):
        project = self.get_project(project_pk)
        data = request.data.copy()
        data['project'] = project.id

        try:
            Contributor.objects.get(user=data['user'], project=project.id)
            return Response('This user has already been added.', status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = ContributorSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response('This user does not exist.', status=status.HTTP_400_BAD_REQUEST)


class UserContributorsDetailViewSet(APIView):
    permission_classes = [IsAuthenticated, ContributorPermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_object(self, project, contributor_pk):
        return get_object_or_404(Contributor, id=contributor_pk, project=project)

    def delete(self, request, project_pk, contributor_pk):
        project = self.get_project(project_pk)
        contributor = self.get_object(project, contributor_pk)
        if contributor.role == 'AUTHOR':
            return Response('Project author cannot be deleted.', status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class IssuesListViewSet(APIView):
    permission_classes = [IsAuthenticated, IssuePermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_queryset(self, project):
        return Issue.objects.filter(project=project)

    def get(self, request, project_pk):
        project = self.get_project(project_pk)
        issues = self.get_queryset(project)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_pk):
        project = self.get_project(project_pk)
        data = request.data.copy()
        data['project'] = project.id
        data['author'] = request.user.id

        try:
            Contributor.objects.get(id=data['assignee'], project=project.id)
            serializer = IssueSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Contributor.DoesNotExist:
            return Response(
                'This user is not contributing to this project or does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )


class IssuesDetailViewSet(APIView):
    permission_classes = [IsAuthenticated, IssuePermissions]

    def get_project(self, project_pk):
        return get_object_or_404(Project, id=project_pk)

    def get_object(self, project, issue_pk):
        return get_object_or_404(Issue, id=issue_pk, project=project)

    def put(self, request, project_pk, issue_pk):
        project = self.get_project(project_pk)
        issue = self.get_object(project, issue_pk)
        data = request.data.copy()
        data['project'] = project.id
        data['author'] = issue.author.id

        try:
            Contributor.objects.get(id=data['assignee'], project=project.id)
            serializer = IssueSerializer(issue, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Contributor.DoesNotExist:
            return Response(
                'This user is not contributing to this project or does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, project_pk, issue_pk):
        project = self.get_project(project_pk)
        issue = self.get_object(project, issue_pk)
        issue.delete()
        return Response('Issue successfully deleted.', status=status.HTTP_204_NO_CONTENT)


class CommentListViewSet(APIView):
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_project_and_issue(self, project_pk, issue_pk):
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        return project, issue

    def get_queryset(self, project, issue):
        return Comment.objects.filter(issue=issue)

    def get(self, request, project_pk, issue_pk):
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        comments = self.get_queryset(project, issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_pk, issue_pk):
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailViewSet(APIView):
    permission_classes = [IsAuthenticated, CommentPermissions]

    def get_project_and_issue(self, project_pk, issue_pk):
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        return project, issue

    def get_object(self, project, issue, comment_pk):
        return get_object_or_404(Comment, id=comment_pk, issue=issue)

    def get(self, request, project_pk, issue_pk, comment_pk):
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        comment = self.get_object(project, issue, comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_pk, issue_pk, comment_pk):
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        comment = self.get_object(project, issue, comment_pk)
        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = comment.author.id

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_pk, issue_pk, comment_pk):
        project, issue = self.get_project_and_issue(project_pk, issue_pk)
        comment = self.get_object(project, issue, comment_pk)
        comment.delete()
        return Response('Comment successfully deleted.', status=status.HTTP_204_NO_CONTENT)

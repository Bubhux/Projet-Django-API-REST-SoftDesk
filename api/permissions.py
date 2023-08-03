from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from api.models import Project, Issue, Comment


class ProjectPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs['project_pk'])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == project.author
        except KeyError:
            return True


class ContributorPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        if request.method in permissions.SAFE_METHODS:
            return project in Project.objects.filter(contributors__user=request.user)
        return request.user == project.author


class IssuePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            issue = get_object_or_404(Issue, id=view.kwargs['issue_pk'])
            return request.user == issue.author
        except KeyError:
            return project in Project.objects.filter(contributors__user=request.user)


class CommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['project_pk'])
        try:
            comment = get_object_or_404(Comment, id=view.kwargs['comment_pk'])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == comment.author
        except KeyError:
            return project in Project.objects.filter(contributors__user=request.user)

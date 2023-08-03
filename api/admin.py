from django.contrib import admin
from api.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):

    list_display = ('title', 'description', 'type')


class ContributorAdmin(admin.ModelAdmin):

    list_display = ('user_id', 'project_id', 'role')


class IssueAdmin(admin.ModelAdmin):

    list_display = ('title', 'description', 'priority', 'tag', 'status')


class CommentAdmin(admin.ModelAdmin):

    list_display = ('description', 'created_time')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
from django.contrib import admin
from django.contrib.auth.models import Group

from api.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'tag', 'status', 'author', 'assignee')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','description', 'issue', 'created_time')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count_in_staff_group')

    def user_count_in_staff_group(self, obj):
        staff_group = Group.objects.get(name='Staff')
        return staff_group.user_set.count()

    user_count_in_staff_group.short_description = 'Nombre d\'utilisateurs dans le groupe Staff'


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)

# Enregistrer le nouveau admin.ModelAdmin pour Group
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

from django.contrib import admin

from .models import User
from .utils import contributed_projects_count

class UserAdmin(admin.ModelAdmin):
    """
    Administration des utilisateurs.

    Cette classe personnalisée définit l'affichage et les fonctionnalités
    de l'interface d'administration pour le modèle User.
    """
    list_display = ['username', 'email', 'is_staff', 'is_active', 'age', 'contributed_projects_count']
    list_filter = ('username', 'is_superuser', 'is_staff', 'groups', 'is_active')
    readonly_fields = ['date_joined']

    def contributed_projects_count(self, obj):
        return obj.contributor_set.count()

    contributed_projects_count.short_description = 'Nombre de projets contribués'

admin.site.register(User, UserAdmin)

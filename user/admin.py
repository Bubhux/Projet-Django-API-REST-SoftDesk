from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'is_staff', 'is_active', 'age']
    list_filter = ('username', 'is_superuser', 'is_staff', 'is_active')

admin.site.register(User, UserAdmin)

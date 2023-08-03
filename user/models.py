from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _

from api.models import Contributor


def validate_min_age(value):
    min_age = 15
    if value < min_age:
        raise ValidationError(_("L'âge ne peut pas être inférieur à %d ans.") % min_age)


class UserManager(BaseUserManager):
    """Gestionnaire de modèle personnalisé pour la classe User"""

    REQUIRED_FIELDS = ['age', 'consent_choice']  # Champs requis pour la création d'un utilisateur

    def create_user(self, username, password, age, consent_choice, **extra_fields):
        """Méthode pour créer un utilisateur régulier"""

        if not username:
            raise ValueError('Vous devez entrer un nom.')
        if not password:
            raise ValueError('Vous devez fournir un mot de passe.')

        if age is None or consent_choice is None:
            raise ValueError('Vous devez fournir l\'âge et le consentement.')

        if age < 15:
            raise ValidationError(_("L'âge ne peut pas être inférieur à 15 ans."))

        extra_fields.setdefault('is_active', True)

        # Créer l'utilisateur et le sauvegarder dans la base de données
        user = self.model(username=username, age=age, consent_choice=consent_choice, **extra_fields)
        user.set_password(password)
        user.save()

        # Afficher les détails du nouvel utilisateur créé
        print(f"Nouvel utilisateur créé : {user.username}")
        print(f"Statut 'is_staff' de l'utilisateur : {user.is_staff}")

        # Vérifier s'il est dans un groupe et afficher les groupes s'il y en a
        if user.groups.exists():
            groups_list = ", ".join([group.name for group in user.groups.all()])
            print(f"Groupes de l'utilisateur : {groups_list}")
        else:
            print("L'utilisateur n'appartient à aucun groupe.")
        return user

    def create_superuser(self, username, password, age, consent_choice, **extra_fields):
        """Méthode pour créer un superutilisateur"""

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if age is None or consent_choice is None:
            raise ValueError('Vous devez fournir l\'âge et le consentement pour le superutilisateur.')

        if age < 15:
            raise ValidationError(_("L'âge ne peut pas être inférieur à 15 ans."))

        # Créer le superutilisateur et le sauvegarder dans la base de données
        superuser = self.model(username=username, age=age, consent_choice=consent_choice, **extra_fields)
        superuser.set_password(password)
        superuser.save()

        # Afficher les détails du nouvel utilisateur superutilisateur créé
        print(f"Nouveau superutilisateur créé : {username}")
        print(f"Statut 'is_superuser' du superutilisateur : {extra_fields['is_superuser']}")

        # Vérifier s'il est dans un groupe et afficher les groupes s'il y en a
        if superuser.groups.exists():
            groups_list = ", ".join([group.name for group in user.groups.all()])
            print(f"Groupes du superutilisateur : {groups_list}")
        else:
            print("Le superutilisateur n'appartient à aucun groupe.")
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle d'utilisateur personnalisé"""

    username = models.CharField(max_length=128, unique=True)  # Utilisation du champ "username" pour le nom d'utilisateur
    age = models.PositiveIntegerField(validators=[validate_min_age])
    consent_choice = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)  # Champ e-mail facultatif
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # Champ pour stocker le nombre de projets contribués par l'utilisateur
    contributed_projects_count = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'username'  # Utilisation du champ "username" pour l'authentification
    REQUIRED_FIELDS = ['age', 'consent_choice']  # Champs requis pour la création d'un utilisateur

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        """Méthode pour vérifier si l'utilisateur a une permission particulière"""
        return True

    def has_module_perms(self, app_label):
        """Méthode pour vérifier si l'utilisateur a des permissions pour un module d'application"""
        return True

    def __str__(self):
        """Méthode pour représenter l'objet sous forme de chaîne de caractères"""
        return self.username

    def save(self, *args, **kwargs):
        """Méthode pour sauvegarder l'objet User dans la base de données"""
        super(User, self).save(*args, **kwargs)

    @property
    def contributed_projects_count(self):
        """Retourne le nombre de projets auxquels l'utilisateur a contribué"""
        return self.contributor_set.values('project').distinct().count()

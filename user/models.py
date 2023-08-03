from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_min_age(value):
    min_age = 15
    if value < min_age:
        raise ValidationError(_("L'âge ne peut pas être inférieur à %d ans.") % min_age)


class User(AbstractUser):
    """Classe utilisateur personnalisée basée sur AbstractUser"""

    # Nouveaux champs personnalisés
    age = models.PositiveIntegerField(validators=[validate_min_age])
    consent_choice = models.BooleanField()

    # Champs pour l'interface d'administration de Django
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def clean(self):
        if self.age < 15:
            raise ValidationError(_("L'âge ne peut pas être inférieur à 15 ans."))
        if not self.consent_choice:
            raise ValidationError(_("Le consentement est obligatoire."))
        super().clean()


@receiver(post_save, sender=User)
def set_new_user_as_staff(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        instance.is_staff = True
        instance.save()

        # Ajouter le nouvel utilisateur au groupe "Staff"
        staff_group = Group.objects.get(name='Staff')
        instance.groups.add(staff_group)

        # Débogage
        print(f"Nouvel utilisateur créé : {instance.username}")
        print(f"Statut 'is_staff' de l'utilisateur : {instance.is_staff}")
        print(f"Groupes de l'utilisateur : {instance.groups.all()}")




from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


def validate_min_age(value):
    min_age = 15
    if value < min_age:
        raise ValidationError(_("L'âge ne peut pas être inférieur à %d ans.") % min_age)


class User(AbstractUser):
    """Classe utilisateur personnalisée basée sur AbstractUser"""

    # Nouveaux champs personnalisés
    age = models.PositiveIntegerField(validators=[validate_min_age])
    consent_choice = models.BooleanField()

    def clean(self):
        if self.age < 15:
            raise ValidationError(_("L'âge ne peut pas être inférieur à 15 ans."))
        if not self.consent_choice:
            raise ValidationError(_("Le consentement est obligatoire."))
        super().clean()


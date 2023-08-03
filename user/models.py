from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class MinAgeValidator:
    def __init__(self, min_age):
        self.min_age = min_age

    def __call__(self, value):
        if value < self.min_age:
            raise ValidationError(_("L'âge ne peut pas être inférieur à %d ans.") % self.min_age)


class User(AbstractUser):
    """Classe utilisateur personnalisée basée sur AbstractUser"""

    # Nouveaux champs personnalisés
    age = models.PositiveIntegerField(validators=[MinAgeValidator(15)])
    consent_choice = models.BooleanField()

    def clean(self):
        if self.age < 15:
            raise ValidationError(_("L'âge ne peut pas être inférieur à 15 ans."))
        if self.consent_choice is False:
            raise ValidationError(_("Le consentement est obligatoire."))
        super().clean()

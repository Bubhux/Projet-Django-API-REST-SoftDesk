from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from . models import User, MinAgeValidator

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    """Champ personnalisé pour stocker les jetons d'authentification"""
    tokens = SerializerMethodField()

    class Meta:
        model = User
        # Champs du modèle User à inclure dans la sérialisation
        fields = ['username', 'email', 'password', 'age', 'consent_choice']

    def validate_password(self, value):
        # Méthode de validation personnalisée pour le champ password
        if value is not None:
            # Vérifier que le mot de passe n'est pas vide
            return make_password(value)  # Hacher le mot de passe avant de le sauvegarder
        raise ValidationError("Password is empty")  # Le mot de passe est vide, lever une erreur de validation

    def get_tokens(self, user):
        # Méthode pour obtenir les jetons (tokens) d'authentification pour l'utilisateur
        tokens = RefreshToken.for_user(user)  # Générer les jetons à l'aide de Django REST framework simplejwt
        data = {
            "refresh": str(tokens),  # Convertir le jeton d'actualisation en chaîne
            "access": str(tokens.access_token)  # Convertir le jeton d'accès en chaîne
        }
        return data  # Retourner le dictionnaire contenant les jetons

    def create(self, validated_data):
        # Méthode pour créer un nouvel utilisateur dans la base de données
        user = User.objects.create_user(
            username=validated_data['username'],  # Récupérer le nom d'utilisateur à partir des données validées
            email=validated_data['email'],  # Récupérer l'email à partir des données validées
            age=validated_data['age'],  # Récupérer l'âge à partir des données validées
            consent_choice=validated_data['consent_choice'],  # Récupérer le choix du consentement à partir des données validées
        )
        user.set_password(validated_data['password'])  # Définir le mot de passe haché à partir des données validées
        user.save()
        return user

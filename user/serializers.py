from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField

from . models import User, validate_min_age

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    """Champ personnalisé pour stocker les jetons d'authentification"""
    tokens = SerializerMethodField()

    class Meta:
        model = User
        # Champs du modèle User à inclure dans la sérialisation
        fields = ['username', 'email', 'password', 'age', 'consent_choice', 'tokens']

    def validate_password(self, value):
        """Méthode de validation personnalisée pour le champ password"""
        # Vérifier que le mot de passe n'est pas vide
        if value is not None:
            # Hacher le mot de passe avant de le sauvegarder
            return make_password(value)
        # Le mot de passe est vide, lever une erreur de validation
        raise ValidationError("Password is empty")

    def get_tokens(self, user):
        """Méthode pour obtenir les jetons (tokens) d'authentification pour l'utilisateur"""

        # Générer les jetons à l'aide de Django REST framework simplejwt
        tokens = RefreshToken.for_user(user) 
        data = {
            "refresh": str(tokens),  # Convertir le jeton d'actualisation en chaîne
            "access": str(tokens.access_token)  # Convertir le jeton d'accès en chaîne
        }
        # Retourner le dictionnaire contenant les jetons
        return data 

    def create(self, validated_data):
        """Méthode pour créer un nouvel utilisateur dans la base de données"""

        # Récupérer le nom d'utilisateur à partir des données validées
        # Récupérer l'email à partir des données validées
        # Récupérer l'âge à partir des données validées
        # Récupérer le choix du consentement à partir des données validées
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'], 
            age=validated_data['age'], 
            consent_choice=validated_data['consent_choice'],
        )
        # Définir le mot de passe haché à partir des données validées
        user.set_password(validated_data['password'])
        user.save()
        return user


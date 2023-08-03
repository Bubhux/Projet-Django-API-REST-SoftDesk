from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . serializers import UserSignupSerializer

User = get_user_model()

class SignupView(APIView):
    """
    Vue pour l'inscription des utilisateurs.

    Cette vue permet à un utilisateur de s'inscrire en fournissant un nom d'utilisateur,
    une adresse e-mail, un mot de passe, l'âge et le consentement. L'utilisateur sera créé dans la base de données
    avec les informations fournies.
    """
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

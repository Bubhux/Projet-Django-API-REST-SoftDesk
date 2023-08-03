"""SoftDesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.views import SignupView
from api.views import (
    ProjectViewSet,
    UserContributorsViewSet,
    IssueViewSet,
    CommentViewSet
)


# Création du routeur simple
router = SimpleRouter()

# Enregistrement des vues avec le routeur simple
# Ne pas utiliser .as_view() pour les ViewSets enregistrées avec le routeur
router.register(r"projects", ProjectViewSet, basename="projects")
#router.register(r"project-detail", ProjectViewSet, basename="project-detail")

router.register(r"users", UserContributorsViewSet, basename="users")
#router.register(r"user-contributors-detail", UserContributorsDetailViewSet, basename="user-contributors-detail")

router.register(r"issues", IssueViewSet, basename="issues")
#router.register(r"issue-detail", IssueDetailViewSet, basename="issue-detail")

router.register(r"comments", CommentViewSet, basename="comments")
#router.register(r"comment-detail", CommentDetailViewSet, basename="comment-detail")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    path('api/projects/', ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-list'),
    path('api/projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='project-detail'),

    path('api/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'create'}), name='issue-list'),
    path('api/issues/<int:pk>/', IssueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='issue-detail'),

    path('api/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('api/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='comment-detail'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "api/"
    path('api/', include(router.urls))
]

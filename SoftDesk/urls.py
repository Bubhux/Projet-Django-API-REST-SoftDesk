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
from rest_framework_simplejwt.views import TokenObtainPairView

from user.views import SignupView
from api.views import (
    ProjectListViewSet,
    ProjectDetailViewSet,
    UserContributorsListViewSet,
    UserContributorsDetailViewSet,
    IssueListViewSet,
    IssueDetailViewSet,
    CommentListViewSet,
    CommentDetailViewSet
)


# Création du routeur simple
router = SimpleRouter()

# Enregistrement des vues avec le routeur simple
router.register(r"users", UserContributorsListViewSet, basename="users")
router.register(r"user-contributors-detail", UserContributorsDetailViewSet, basename="user-contributors-detail")

router.register(r"issues", IssueListViewSet, basename="issues")
router.register(r"issue-detail", IssueDetailViewSet, basename="issue-detail")

router.register(r"comments", CommentListViewSet, basename="comments")
router.register(r"comment-detail", CommentDetailViewSet, basename="comment-detail")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),

    path('api/projects/', ProjectListViewSet.as_view(), name='project-list'),
    path('api/projects/<int:pk>/', ProjectDetailViewSet.as_view(), name='project-detail'),

    path('api/issues/', IssueListViewSet.as_view(), name='issue-list'),
    path('api/issues/<int:pk>/', IssueDetailViewSet.as_view(), name='issue-detail'),

    path('api/comments/', CommentListViewSet.as_view(), name='comment-list'),
    path('api/comments/<int:pk>/', CommentDetailViewSet.as_view(), name='comment-detail'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "api/"
    path('api/', include(router.urls))
]

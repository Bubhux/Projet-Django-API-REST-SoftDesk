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
    CommentViewSet,
    AdminUserViewSet,
    AdminProjectViewSet,
    AdminUserContibutorViewSet,
    AdminIssueViewSet,
    AdminCommentViewSet
)

# Création du routeur simple
router = SimpleRouter()

# Enregistrement des vues avec le routeur simple
router.register(r"projects", ProjectViewSet, basename="projects")
router.register(r"projects/(?P<project_pk>\d+)/users", UserContributorsViewSet, basename="users")
#router.register(r"projects/(?P<project_pk>\d+)/users/(?P<contributor_pk>\d+)", UserContributorsViewSet, basename="projects-users")
router.register(r'projects/(?P<project_pk>\d+)/users/(?P<contributor_pk>\d+)', UserContributorsViewSet, basename='projects-users')

router.register(r"projects/(?P<project_pk>\d+)/issues", IssueViewSet, basename="issues")
router.register(r"projects/(?P<project_pk>\d+)/issues/(?P<issue_pk>\d+)/comments", CommentViewSet, basename="projects-issues")
router.register(r"projects/(?P<project_pk>\d+)/issues/(?P<issue_pk>\d+)/comments/(?P<comment_pk>\d+)", CommentViewSet, basename="projects-issues-comments")
#router.register(r"projects/(?P<project_pk>\d+)/issues/(?P<issue_pk>\d+)/comments/(?P<comment_pk>\d+)/update_comment", CommentViewSet, basename="update-comment")


router.register(r"admin/users", AdminUserViewSet, basename="admin-users")
router.register(r"admin/projects", AdminProjectViewSet, basename="admin-projects")
router.register(r"admin/contributors", AdminUserContibutorViewSet, basename="admin-contributors")
router.register(r"admin/issues", AdminIssueViewSet, basename="admin-issues")
router.register(r"admin/comments", AdminCommentViewSet, basename="admin-comments")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    # Inclusion des URLs gérées par le routeur simple sous le préfixe "api/"
    path('api/', include(router.urls))
]

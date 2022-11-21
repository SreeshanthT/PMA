from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from PMA_api.views import (
    UserViewSet,ListUsers,RegisterUser,SignInUser,
    PasswordView,SharePasswordView,IndexView
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', IndexView.as_view(), name='index'),
    path('list-users/', ListUsers.as_view(),name='list_users'),
    path('api-token-auth/', views.obtain_auth_token),
    path('sign-in/', SignInUser.as_view(), name="sign_in"),
    path('sign-up/', RegisterUser.as_view(),name='sign_up'),
    
    path('password/', PasswordView.as_view(),name='password_create'),
    path('password/<str:pk>/', PasswordView.as_view(),name='password_create'),
    
    path('share-password/', SharePasswordView.as_view(),name='share_password'),
]
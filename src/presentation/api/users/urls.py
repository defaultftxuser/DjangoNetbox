from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from src.presentation.api.users.views import RegisterView, LogoutView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

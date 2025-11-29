from django.urls import path
from .views import register, login, logout, get_profile, patch_profile

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('me/', get_profile),
    path('me/patch', patch_profile),
]

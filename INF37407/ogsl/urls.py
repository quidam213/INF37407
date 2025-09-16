##
## EPITECH PROJECT, 2025
## INF37407
## File description:
## urls.py
##

from django.urls import path
from ogsl.views import root, param, converter, convertResult

urlpatterns = [
    path('', root),
    path('param/<str:test>', param),
    path('converter', converter),
    path('converter/<str:optInitial>/<int:nInitial>', convertResult)
]

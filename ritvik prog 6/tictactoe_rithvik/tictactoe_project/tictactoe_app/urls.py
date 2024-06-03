from django.urls import path
from . import views

urlpatterns = [
    path('x/', views.x, name='x'),
    path('o/', views.o, name='o'),
    path('game/', views.game, name='game'),
]

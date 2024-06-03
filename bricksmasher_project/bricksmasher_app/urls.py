# bricksmasher_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rental/<int:email_id>/<int:movie_id>/', views.rent, name='rent'), #lolololo
    path('account.html/', views.account, name='account'),
    path('movie.html/', views.movie, name='movie'),
    path('rent.html/', views.rent, name='rent'),
    path('dbUser/', views.db_user, name='db_user'),
    path('dbMovie/', views.db_movie, name='db_movie'),
    path('dbRent/', views.db_rent, name='db_rent'),
]

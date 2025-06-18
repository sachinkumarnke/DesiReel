from django.urls import path
from .admin_views import admin_movie_analytics

urlpatterns = [
    path('movie-analytics/', admin_movie_analytics, name='movie-analytics'),
]
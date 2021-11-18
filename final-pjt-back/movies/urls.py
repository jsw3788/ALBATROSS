from django.urls import path
from . import views

urlpatterns = [
    path('movies/popularity/', views.read_movies_by_popularity),
    path('movies/score/', views.read_movies_by_score),
    path('movies/release_date/', views.read_movies_by_release),
    path('movies/recommend/', views.read_movies_by_recommend),

    path('database/genres/', views.get_genre),
    path('database/movies/', views.get_movies),
    path('database/credits/', views.get_credits)
]

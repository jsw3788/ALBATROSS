from django.urls import path
from . import views

urlpatterns = [
    path('database/genres/', views.get_genre),
    path('database/movies/', views.get_movies),
    path('database/credits/', views.get_credits)
]

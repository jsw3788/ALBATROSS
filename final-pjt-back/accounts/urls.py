from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('<username>/profile/', views.profile),
    path('<username>/follow/', views.follow),
    # path('api-token-auth/', obtain_jwt_token),
]

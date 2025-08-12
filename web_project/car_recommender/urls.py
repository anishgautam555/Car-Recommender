from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("standard-recommender", views.standard, name="standard-recommender"),
    path("simple-recommender", views.simple, name="simple-recommender"),
]
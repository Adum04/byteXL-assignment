from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("weather/", views.weather),
    path("convert/", views.convert),
    path("quote/", views.quote),
]

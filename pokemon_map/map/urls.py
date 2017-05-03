from django.conf.urls import url 
from . import views

urlpatterns = [
    # For all requests, call the view function named pokemons(request)
    url(r'^', views.pokemons, name = 'pokemons'),
]

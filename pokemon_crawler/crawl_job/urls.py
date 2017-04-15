from django.conf.urls import url 
from . import views

urlpatterns = [
    # For all requests, call the view function named add_crawl_point(request)
    url(r'^', views.add_crawl_point, name = 'add_crawl_point'),
]

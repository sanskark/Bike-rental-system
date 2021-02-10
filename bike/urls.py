from django.urls import path
from . import views

urlpatterns = [
    path('bikeslist/', views.bikes_list, name="bikes-list"),
]
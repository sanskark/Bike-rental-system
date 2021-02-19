from django.urls import path
from . import views

urlpatterns = [
    path('bikeslist/', views.bikes_list, name="bikes-list"),
    path('booking/', views.booking, name="bike-booking"),
    path('confirmbooking/', views.confirm_booking, name="bike-confirmbooking"),
]
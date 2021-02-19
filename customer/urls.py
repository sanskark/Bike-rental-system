from django.urls import path
from . import views

urlpatterns =[
    path('signup/', views.customer_signup.as_view(), name='customer-signup'),
    path('login/', views.customer_login, name='customer-login'),
    path('logout/', views.customer_logout, name='customer-logout'),
    path('profile/', views.profile, name='customer-profile'),
    path('myrides/', views.my_rides, name='customer-myrides')
]
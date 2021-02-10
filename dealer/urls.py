from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.dealer_register.as_view(), name='dealer-register'),
    path('login/', views.dealer_login, name='dealer-login'),
    path('logout/', views.dealer_logout, name='dealer-logout'),
    path('profile/', views.profile, name='dealer-profile'),
    path('addbike/', views.add_bike, name='dealer-addbike'),
    path('addnewbike/', views.add_new_bike, name='dealer-addnewbike'),
    path('mybikes/', views.my_bikes, name='dealer-mybikes'),
    path('mybikes/deletebike/', views.delete_bike, name='dealer-deletebike'),
    path('mybikes/editbike/', views.edit_bike, name='dealer-editbike'),
    path('mybikes/applybike/', views.apply_bike, name='dealer-applybike'),
    path('mybikes/holdbike/', views.hold_bike, name='dealer-holdbike'),
]
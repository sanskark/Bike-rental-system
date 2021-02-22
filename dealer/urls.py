from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('bookings/',views.dealer_bookings, name="dealer-bookings"),
    path('bookings/customer_details',views.customer_details, name="dealer-customerdetails"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name= 'dealer/password_reset.html'),
         name='password_reset_dealer'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name= 'dealer/password_reset_done.html'),
         name='password_reset_done_dealer'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name= 'dealer/password_reset_confirm.html'),
         name='password_reset_confirm_dealer'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name= 'dealer/password_reset_complete.html'),
         name='password_reset_complete_dealer')
]
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns =[
    path('signup/', views.customer_signup.as_view(), name='customer-signup'),
    path('login/', views.customer_login, name='customer-login'),
    path('logout/', views.customer_logout, name='customer-logout'),
    path('profile/', views.profile, name='customer-profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name= 'customer/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name= 'customer/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name= 'customer/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name= 'customer/password_reset_complete.html'),
         name='password_reset_complete'),
    path('myrides/', views.my_rides, name='customer-myrides'),
    path('myrides/cancel', views.cancel_booking, name='customer-cancelbooking'),
]
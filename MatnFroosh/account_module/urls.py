from django.urls import path
from . import views

urlpatterns = [
    path('account-activation/<str:email_active_code>/', views.account_activation, name='account_activation_page'),
    path('forgot-password/', views.ForgotPassword_view.as_view(), name='forgot_password_page'),
    path('forgot-password/<str:email_active_code>/', views.ForgotPassword_view.as_view(), name='edit_password_page'),
]
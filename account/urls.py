from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/verify/', views.verify_email, name='verify_email'),
    path('register/verify/resend/',views.resend_email, name='resend_verification_email'),
]

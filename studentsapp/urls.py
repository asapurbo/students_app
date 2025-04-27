from django.urls import path
from studentsapp import views

app_name = 'studentsapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.form, name='form'),
    path('pdf/', views.student_pdf, name='student_pdf'),
    path('signature/', views.signature, name='signature'),
]


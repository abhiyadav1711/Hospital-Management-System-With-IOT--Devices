from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('patients/', views.patients_view, name='patients'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
]
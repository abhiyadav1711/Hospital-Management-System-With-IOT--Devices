from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('patients/', views.patients_view, name='patients'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('monitoring/', views.monitoring_view, name='monitoring'),
    path('doctors/', views.doctors_view, name='doctors'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('doctors/<int:pk>/toggle/', views.doctor_toggle_availability, name='doctor_toggle'),
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    path('emergency/', views.emergency_view, name='emergency'),
    path('billing/', views.billing_view, name='billing'),
    path('reports/', views.reports_view, name='reports'),
]
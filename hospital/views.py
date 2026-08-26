from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Patient, Doctor, Appointment, Bill


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'hospital/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_beds = 40
    occupied = Patient.objects.exclude(status='Discharged').count()
    critical_patients = Patient.objects.filter(status='Critical')
    total_revenue = sum(b.total for b in Bill.objects.all())

    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'today_appointments': Appointment.objects.filter(date=date.today()).count(),
        'available_beds': total_beds - occupied,
        'emergency_cases': critical_patients.count(),
        'total_revenue': total_revenue,
        'recent_appointments': Appointment.objects.select_related('patient', 'doctor')[:5],
        'patients': Patient.objects.all(),
        'today': date.today(),
    }
    return render(request, 'hospital/dashboard.html', context)
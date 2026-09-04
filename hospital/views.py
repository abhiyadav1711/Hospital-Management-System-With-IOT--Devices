from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Patient, Doctor, Appointment, Bill, VitalReading
from django.shortcuts import get_object_or_404


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
@login_required
def patients_view(request):
    if request.method == 'POST':
        pid = request.POST.get('patient_id')
        data = dict(
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            disease=request.POST.get('disease'),
            status=request.POST.get('status'),
            contact=request.POST.get('contact'),
            device_id=request.POST.get('device_id') or None,
        )
        if pid:
            Patient.objects.filter(id=pid).update(**data)
            messages.success(request, f"{data['name']} updated.")
        else:
            Patient.objects.create(**data)
            messages.success(request, f"{data['name']} added.")
        return redirect('patients')

    search = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    qs = Patient.objects.all()
    if search:
        qs = qs.filter(name__icontains=search) | qs.filter(disease__icontains=search)
    if status_filter:
        qs = qs.filter(status=status_filter)

    return render(request, 'hospital/patients.html', {
        'patients': qs.order_by('-created_at'), 'search': search, 'status_filter': status_filter,
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    messages.success(request, f"{patient.name} deleted.")
    return redirect('patients')

@login_required
def monitoring_view(request):
    patients = Patient.objects.all()
    return render(request, 'hospital/monitoring.html', {'patients': patients})
@login_required
def doctors_view(request):
    if request.method == 'POST':
        did = request.POST.get('doctor_id')
        data = dict(
            name=request.POST.get('name'),
            specialization=request.POST.get('specialization'),
            experience_years=request.POST.get('experience_years') or 0,
            availability=request.POST.get('availability'),
        )
        if did:
            Doctor.objects.filter(id=did).update(**data)
            messages.success(request, f"Dr. {data['name']} updated.")
        else:
            Doctor.objects.create(**data)
            messages.success(request, f"Dr. {data['name']} added.")
        return redirect('doctors')

    return render(request, 'hospital/doctors.html', {'doctors': Doctor.objects.all()})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.delete()
    messages.success(request, f"Dr. {doctor.name} removed.")
    return redirect('doctors')


@login_required
def doctor_toggle_availability(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.availability = 'Busy' if doctor.availability == 'Available' else 'Available'
    doctor.save()
    return redirect('doctors')

@login_required
def appointments_view(request):
    if request.method == 'POST':
        Appointment.objects.create(
            patient_id=request.POST.get('patient'),
            doctor_id=request.POST.get('doctor'),
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            status='Confirmed',
        )
        messages.success(request, "Appointment booked.")
        return redirect('appointments')

    return render(request, 'hospital/appointments.html', {
        'appointments': Appointment.objects.select_related('patient', 'doctor'),
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
    })


@login_required
def appointment_cancel(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    appt.status = 'Cancelled'
    appt.save()
    return redirect('appointments')
@login_required
def emergency_view(request):
    critical = [p for p in Patient.objects.all() if p.latest_vitals and p.latest_vitals.status_level == 'red']
    return render(request, 'hospital/emergency.html', {'critical_patients': critical})

@login_required
def billing_view(request):
    if request.method == 'POST':
        Bill.objects.create(
            patient_id=request.POST.get('patient'),
            consultation_fee=request.POST.get('consultation_fee') or 0,
            room_charges=request.POST.get('room_charges') or 0,
            medicine_charges=request.POST.get('medicine_charges') or 0,
            payment_status=request.POST.get('payment_status'),
        )
        messages.success(request, "Bill generated.")
        return redirect('billing')

    return render(request, 'hospital/billing.html', {
        'bills': Bill.objects.select_related('patient'),
        'patients': Patient.objects.all(),
    })
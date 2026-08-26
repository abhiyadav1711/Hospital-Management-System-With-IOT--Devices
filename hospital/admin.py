from django.contrib import admin
from .models import Patient, Doctor, Appointment, VitalReading, Bill


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'disease', 'status', 'device_id')
    list_filter = ('status', 'gender')
    search_fields = ('name', 'disease', 'device_id')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'experience_years', 'availability')
    list_filter = ('availability', 'specialization')
    search_fields = ('name', 'specialization')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date')


@admin.register(VitalReading)
class VitalReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'heart_rate', 'spo2', 'temperature', 'timestamp', 'status_level')
    list_filter = ('patient',)
    readonly_fields = ('timestamp',)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'total', 'payment_status', 'created_at')
    list_filter = ('payment_status',)
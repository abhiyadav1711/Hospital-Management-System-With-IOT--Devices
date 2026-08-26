from django.db import models
from django.utils import timezone
class Doctor(models.Model):
    AVAILABILITY_CHOICES = [('Available', 'Available'), ('Busy', 'Busy')]

    name = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120)
    experience_years = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='Available')

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Patient(models.Model):
    STATUS_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Discharged', 'Discharged'),
        ('Critical', 'Critical'),
    ]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    name = models.CharField(max_length=120)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    disease = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Admitted')
    contact = models.CharField(max_length=20, blank=True)
    device_id = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                  help_text="ESP32 device ID sending this patient's vitals, e.g. ESP32-01")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    @property
    def patient_code(self):
        return f"PT-{1000 + self.id}"
    @property
    def latest_vitals(self):
        return self.vitals.order_by('-timestamp').first()
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Waiting', 'Waiting'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.date}"
class VitalReading(models.Model):
    """
    One row = one reading pushed by an IoT device (ESP32 + sensors).
    The ESP32 will POST JSON to /api/vitals/ with these fields.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vitals')
    heart_rate = models.PositiveIntegerField(help_text="BPM")
    spo2 = models.PositiveIntegerField(help_text="Blood oxygen %")
    temperature = models.FloatField(help_text="Body temp in Fahrenheit")
    bp_systolic = models.PositiveIntegerField(default=120)
    bp_diastolic = models.PositiveIntegerField(default=80)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.patient.name} @ {self.timestamp:%H:%M:%S} — {self.heart_rate} BPM"

    @property
    def status_level(self):
        """green / orange / red — used to color the dashboard."""
        if self.heart_rate >= 120 or self.spo2 < 92 or self.temperature >= 101:
            return 'red'
        if self.heart_rate >= 95 or self.spo2 < 95 or self.temperature >= 99.5:
            return 'orange'
        return 'green'


class Bill(models.Model):
    PAYMENT_CHOICES = [('Pending', 'Pending'), ('Paid', 'Paid')]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
    consultation_fee = models.PositiveIntegerField(default=500)
    room_charges = models.PositiveIntegerField(default=0)
    medicine_charges = models.PositiveIntegerField(default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.consultation_fee + self.room_charges + self.medicine_charges

    def __str__(self):
        return f"Bill #{self.id} — {self.patient.name} — ₹{self.total}"
from django.db import models
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
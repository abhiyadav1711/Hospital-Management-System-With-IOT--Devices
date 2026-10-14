from datetime import date, time

from django.core.management.base import BaseCommand

from hospital.models import Appointment, Bill, Doctor, Patient, VitalReading


class Command(BaseCommand):
    help = "Load demo doctors, patients, appointments and bills for presentation."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Delete all existing hospital data before loading demo data.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            for model in (VitalReading, Bill, Appointment, Patient, Doctor):
                model.objects.all().delete()
            self.stdout.write("Old data deleted.")

        if Doctor.objects.exists() or Patient.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Data already exists. Run with --reset to replace it."
            ))
            return

        doctors = [
            Doctor.objects.create(name="Rajesh Sharma", specialization="Cardiology", experience_years=15, availability="Available"),
            Doctor.objects.create(name="Priya Verma", specialization="Neurology", experience_years=10, availability="Busy"),
            Doctor.objects.create(name="Amit Singh", specialization="Orthopedics", experience_years=8, availability="Available"),
            Doctor.objects.create(name="Neha Gupta", specialization="Pediatrics", experience_years=6, availability="Available"),
        ]

        patients = [
            Patient.objects.create(name="Ramesh Kumar", age=58, gender="Male", disease="Heart Disease", status="Admitted", contact="9876500001", device_id="ESP32-01"),
            Patient.objects.create(name="Sunita Devi", age=45, gender="Female", disease="Diabetes", status="Admitted", contact="9876500002", device_id="ESP32-02"),
            Patient.objects.create(name="Mohit Yadav", age=32, gender="Male", disease="Fracture", status="Critical", contact="9876500003", device_id="ESP32-03"),
            Patient.objects.create(name="Anjali Mishra", age=27, gender="Female", disease="Fever", status="Discharged", contact="9876500004"),
            Patient.objects.create(name="Vikas Pandey", age=63, gender="Male", disease="Hypertension", status="Admitted", contact="9876500005"),
        ]

        today = date.today()
        Appointment.objects.create(patient=patients[0], doctor=doctors[0], date=today, time=time(10, 0), status="Confirmed")
        Appointment.objects.create(patient=patients[1], doctor=doctors[3], date=today, time=time(11, 30), status="Waiting")
        Appointment.objects.create(patient=patients[2], doctor=doctors[2], date=today, time=time(14, 0), status="Confirmed")
        Appointment.objects.create(patient=patients[4], doctor=doctors[1], date=today, time=time(16, 0), status="Completed")

        Bill.objects.create(patient=patients[0], consultation_fee=800, room_charges=4500, medicine_charges=1200, payment_status="Pending")
        Bill.objects.create(patient=patients[3], consultation_fee=500, room_charges=0, medicine_charges=300, payment_status="Paid")
        Bill.objects.create(patient=patients[2], consultation_fee=700, room_charges=6000, medicine_charges=2500, payment_status="Pending")

        self.stdout.write(self.style.SUCCESS(
            f"Demo data loaded: {len(doctors)} doctors, {len(patients)} patients. "
            "Devices ESP32-01, ESP32-02, ESP32-03 are linked."
        ))
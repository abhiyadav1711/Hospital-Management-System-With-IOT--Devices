from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Appointment, Doctor, Patient, VitalReading

KEY = 'test-key'


@override_settings(DEVICE_API_KEY=KEY)
class VitalIngestTests(TestCase):
    """Tests for POST /api/vitals/ (the endpoint the ESP32 calls)."""

    def setUp(self):
        Patient.objects.create(name='Test Patient', age=40, disease='Fever', device_id='ESP32-01')
        self.url = reverse('api_vitals_ingest')
        self.normal = {'device_id': 'ESP32-01', 'heart_rate': 80, 'spo2': 98, 'temperature': 98.2}

    def send(self, data, key=None):
        headers = {'HTTP_X_API_KEY': key} if key is not None else {}
        return self.client.post(self.url, data, content_type='application/json', **headers)

    def test_missing_key_is_rejected(self):
        response = self.send(self.normal)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(VitalReading.objects.count(), 0)

    def test_wrong_key_is_rejected(self):
        response = self.send(self.normal, key='wrong-key')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(VitalReading.objects.count(), 0)

    def test_correct_key_saves_reading(self):
        response = self.send(self.normal, key=KEY)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['alert_level'], 'green')
        self.assertEqual(VitalReading.objects.count(), 1)

    def test_critical_values_give_red_alert(self):
        data = dict(self.normal, heart_rate=135, spo2=88, temperature=102.5)
        response = self.send(data, key=KEY)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['alert_level'], 'red')

    def test_unknown_device_is_rejected(self):
        data = dict(self.normal, device_id='NOT-LINKED')
        response = self.send(data, key=KEY)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(VitalReading.objects.count(), 0)


class LoginProtectionTests(TestCase):
    """Pages and dashboard APIs must not open without login."""

    def test_page_redirects_to_login(self):
        response = self.client.get(reverse('patients'))
        self.assertEqual(response.status_code, 302)

    def test_latest_vitals_api_needs_login(self):
        response = self.client.get(reverse('api_vitals_latest'))
        self.assertIn(response.status_code, (401, 403))


class SafeActionTests(TestCase):
    """Delete, cancel and toggle must work only with POST."""

    def setUp(self):
        User.objects.create_user('tester', password='pass12345')
        self.client.login(username='tester', password='pass12345')
        self.patient = Patient.objects.create(name='Ravi', age=30, disease='Cold')
        self.doctor = Doctor.objects.create(name='Asha', specialization='General', availability='Available')
        self.appt = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor,
            date=date.today(), time=time(10, 0), status='Confirmed',
        )

    def test_patient_delete_get_does_nothing(self):
        response = self.client.get(reverse('patient_delete', args=[self.patient.id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Patient.objects.filter(id=self.patient.id).exists())

    def test_patient_delete_post_works(self):
        self.client.post(reverse('patient_delete', args=[self.patient.id]))
        self.assertFalse(Patient.objects.filter(id=self.patient.id).exists())

    def test_doctor_delete_get_does_nothing(self):
        response = self.client.get(reverse('doctor_delete', args=[self.doctor.id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Doctor.objects.filter(id=self.doctor.id).exists())

    def test_doctor_toggle_post_switches_availability(self):
        self.client.post(reverse('doctor_toggle', args=[self.doctor.id]))
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.availability, 'Busy')

    def test_appointment_cancel_get_does_nothing(self):
        response = self.client.get(reverse('appointment_cancel', args=[self.appt.id]))
        self.assertEqual(response.status_code, 405)
        self.appt.refresh_from_db()
        self.assertEqual(self.appt.status, 'Confirmed')

    def test_appointment_cancel_post_works(self):
        self.client.post(reverse('appointment_cancel', args=[self.appt.id]))
        self.appt.refresh_from_db()
        self.assertEqual(self.appt.status, 'Cancelled')
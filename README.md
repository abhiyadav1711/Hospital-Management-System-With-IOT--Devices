# MediPulse - Hospital Management System with IoT Devices

A Django-based hospital management system that also monitors patient vitals live using IoT devices (ESP32 + sensors). Built as a college mini project.

## Features

- Secure login/logout (all pages protected)
- Dashboard with patients, doctors, appointments, beds and revenue stats
- Patient management: add, edit, delete, search and filter by status
- Doctor management with Available/Busy toggle
- Appointment booking and cancellation
- Billing with automatic total calculation
- Reports with charts (Chart.js)
- **Live IoT Monitoring:** heart rate, SpO2, temperature and blood pressure, auto-refreshing every 3 seconds
- **Emergency alerts:** patients with critical vitals are flagged automatically

## Tech Stack

- Backend: Python, Django 4.2, Django REST Framework
- Database: SQLite
- Frontend: Django templates, CSS, JavaScript, Chart.js
- IoT: ESP32 sending JSON over WiFi (HTTP POST)

## Setup

```bash
git clone https://github.com/abhiyadav1711/Hospital-Management-System-With-IOT--Devices.git
cd Hospital-Management-System-With-IOT--Devices
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in with the superuser you created.

## IoT Setup

1. Add a patient and set their **Device ID** (for example `ESP32-01`).
2. The device sends vitals to `POST /api/vitals/` with the header `X-API-Key: medipulse-demo-key`:

```json
{
  "device_id": "ESP32-01",
  "heart_rate": 112,
  "spo2": 96,
  "temperature": 99.1,
  "bp_systolic": 128,
  "bp_diastolic": 84
}
```

3. Open the **Live Monitoring** page to see the data update.

## API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| POST | `/api/vitals/` | Device sends a new reading |
| GET | `/api/vitals/latest/` | Latest vitals of all patients |
| GET | `/api/vitals/history/<patient_id>/` | Last 30 readings of a patient |

## Security

- `POST /api/vitals/` accepts requests only with the correct `X-API-Key` header. The key is set by `DEVICE_API_KEY` in `settings.py` (override it with the `MEDIPULSE_DEVICE_KEY` environment variable).
- All other API endpoints and pages need a logged-in user.

## Alert Levels

| Level | Condition |
|-------|-----------|
| Red | Heart rate >= 120, SpO2 < 92, or temperature >= 101 F |
| Orange | Heart rate >= 95, SpO2 < 95, or temperature >= 99.5 F |
| Green | Everything else |

## Project Structure

```
medipulse/   project settings and root URLs
hospital/    models, views, API, templates, static files
manage.py
requirements.txt
```

## Future Scope

- API token authentication for devices
- SMS/email alerts to doctors
- Vitals history charts per patient
- Deployment on a cloud server
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Patient, VitalReading
from .serializers import VitalIngestSerializer, VitalReadingSerializer


class VitalIngestView(APIView):
    """
    POST /api/vitals/  — called by the ESP32 (or any IoT device).

    Example JSON body sent by the microcontroller:
    {
        "device_id": "ESP32-01",
        "heart_rate": 112,
        "spo2": 96,
        "temperature": 99.1,
        "bp_systolic": 128,
        "bp_diastolic": 84
    }
    """
    def post(self, request):
        serializer = VitalIngestSerializer(data=request.data)
        if serializer.is_valid():
            reading = serializer.save()
            return Response(
                {'status': 'ok', 'reading_id': reading.id, 'alert_level': reading.status_level},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LatestVitalsView(APIView):
    """
    GET /api/vitals/latest/  — used by the dashboard (JS fetch, polled
    every few seconds) to refresh the Live Monitoring cards without a
    full page reload.
    """
    def get(self, request):
        data = []
        for patient in Patient.objects.all():
            reading = patient.latest_vitals
            data.append({
                'patient_id': patient.id,
                'patient_code': patient.patient_code,
                'name': patient.name,
                'status': patient.status,
                'vitals': VitalReadingSerializer(reading).data if reading else None,
            })
        return Response(data)


class PatientVitalsHistoryView(APIView):
    """GET /api/vitals/history/<patient_id>/ — last 30 readings, for charts."""
    def get(self, request, patient_id):
        readings = VitalReading.objects.filter(patient_id=patient_id).order_by('-timestamp')[:30]
        readings = list(reversed(readings))
        return Response(VitalReadingSerializer(readings, many=True).data)
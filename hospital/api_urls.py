from django.urls import path
from . import api_views

urlpatterns = [
    path('vitals/', api_views.VitalIngestView.as_view(), name='api_vitals_ingest'),
    path('vitals/latest/', api_views.LatestVitalsView.as_view(), name='api_vitals_latest'),
    path('vitals/history/<int:patient_id>/', api_views.PatientVitalsHistoryView.as_view(), name='api_vitals_history'),
]
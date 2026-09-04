from rest_framework import serializers
from .models import VitalReading, Patient


class VitalReadingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    status_level = serializers.CharField(read_only=True)

    class Meta:
        model = VitalReading
        fields = [
            'id', 'patient', 'patient_name', 'heart_rate', 'spo2',
            'temperature', 'bp_systolic', 'bp_diastolic', 'timestamp', 'status_level',
        ]
        read_only_fields = ['id', 'timestamp']


class VitalIngestSerializer(serializers.Serializer):
    """
    What the ESP32 actually POSTs. Uses device_id (not the DB patient
    primary key) because that's what's physically flashed onto the
    microcontroller.
    """
    device_id = serializers.CharField(max_length=50)
    heart_rate = serializers.IntegerField()
    spo2 = serializers.IntegerField()
    temperature = serializers.FloatField()
    bp_systolic = serializers.IntegerField(required=False, default=120)
    bp_diastolic = serializers.IntegerField(required=False, default=80)

    def validate_device_id(self, value):
        if not Patient.objects.filter(device_id=value).exists():
            raise serializers.ValidationError(
                f"No patient is linked to device_id '{value}'. "
                f"Set this patient's device_id in Django admin first."
            )
        return value

    def create(self, validated_data):
        patient = Patient.objects.get(device_id=validated_data.pop('device_id'))
        return VitalReading.objects.create(patient=patient, **validated_data)
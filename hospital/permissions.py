import hmac

from django.conf import settings
from rest_framework.permissions import BasePermission


class HasDeviceKey(BasePermission):
    """Allows a request only if it carries the correct X-API-Key header (used by ESP32 devices)."""
    message = 'Invalid or missing X-API-Key.'

    def has_permission(self, request, view):
        expected = getattr(settings, 'DEVICE_API_KEY', '')
        provided = request.headers.get('X-API-Key', '')
        return bool(expected) and hmac.compare_digest(provided, expected)
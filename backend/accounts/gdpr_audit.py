"""Helpers pour l'audit trail des demandes d'accès aux données (SAR)."""

from __future__ import annotations

import hashlib

from django.utils import timezone

from .models import DataRequest


def start_data_request(
    user,
    *,
    request_type: str = DataRequest.RequestType.ACCESS,
    export_format: str = "",
) -> DataRequest:
    """Ouvre une demande SAR et la passe immédiatement en cours de traitement."""
    data_request = DataRequest.objects.create(
        user=user,
        request_type=request_type,
        status=DataRequest.Status.RECEIVED,
        export_format=export_format,
    )
    data_request.status = DataRequest.Status.IN_PROGRESS
    data_request.save(update_fields=["status"])
    return data_request


def complete_data_request(data_request: DataRequest, content: bytes) -> DataRequest:
    """Clôt une demande SAR avec l'empreinte du fichier exporté."""
    data_request.status = DataRequest.Status.RESPONDED
    data_request.export_file_hash = hashlib.sha256(content).hexdigest()
    data_request.responded_at = timezone.now()
    data_request.save(update_fields=["status", "export_file_hash", "responded_at"])
    return data_request

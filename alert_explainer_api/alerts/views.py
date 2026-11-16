import json
import math

from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import api_view

from .serializers import (
    AlertCreateSerializer,
    AlertSerializer,
    ExplainResponseSerializer,
)

from services.explainer import generate_explanation

from .models import Alert

SEVERITIES = {"critical", "warning", "info"}
STRING_FIELDS = ("title", "source", "metric_name")
NUMBER_FIELDS = ("metric_value", "threshold")


def serialize_alert(alert):
    return {
        "id": alert.id,
        "title": alert.title,
        "severity": alert.severity,
        "source": alert.source,
        "metric_name": alert.metric_name,
        "metric_value": alert.metric_value,
        "threshold": alert.threshold,
        "created_at": alert.created_at,
    }


def parse_alert_payload(request):
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, JsonResponse({"detail": "Invalid JSON body"}, status=422)

    if not isinstance(payload, dict):
        return None, JsonResponse({"detail": "Expected a JSON object"}, status=422)

    missing = [
        field
        for field in (*STRING_FIELDS, "severity", *NUMBER_FIELDS)
        if field not in payload
    ]
    if missing:
        return None, JsonResponse(
            {"detail": f"Missing required fields: {', '.join(missing)}"}, status=422
        )

    if any(not isinstance(payload[field], str) for field in STRING_FIELDS):
        return None, JsonResponse(
            {"detail": "title, source, and metric_name must be strings"}, status=422
        )
    if not isinstance(payload["severity"], str) or payload["severity"] not in SEVERITIES:
        return None, JsonResponse(
            {"detail": "severity must be critical, warning, or info"}, status=422
        )

    values = {field: payload[field] for field in STRING_FIELDS}
    values["severity"] = payload["severity"]
    for field in NUMBER_FIELDS:
        value = payload[field]
        if isinstance(value, bool):
            return None, JsonResponse(
                {"detail": f"{field} must be a finite number"}, status=422
            )
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None, JsonResponse(
                {"detail": f"{field} must be a finite number"}, status=422
            )
        if not math.isfinite(value):
            return None, JsonResponse(
                {"detail": f"{field} must be a finite number"}, status=422
            )
        values[field] = value

    return values, None


@extend_schema_view(
    get=extend_schema(responses=AlertSerializer(many=True)),
    post=extend_schema(
        request=AlertCreateSerializer,
        responses={201: AlertSerializer},
    ),
)
@api_view(["GET", "POST"])
def alert_collection(request):
    if request.method == "GET":
        alerts = Alert.objects.order_by("id")
        return JsonResponse([serialize_alert(alert) for alert in alerts], safe=False)

    values, error = parse_alert_payload(request)
    if error is not None:
        return error

    alert = Alert.objects.create(**values)
    return JsonResponse(serialize_alert(alert), status=201)


@extend_schema(responses=AlertSerializer)
@api_view(["GET"])
def alert_detail(request, alert_id):
    try:
        alert = Alert.objects.get(pk=alert_id)
    except Alert.DoesNotExist:
        return JsonResponse({"detail": "Alert not found"}, status=404)
    return JsonResponse(serialize_alert(alert))


@extend_schema_view(
    post=extend_schema(request=None, responses=ExplainResponseSerializer)
)
@api_view(["POST"])
def explain_alert(request, alert_id):
    try:
        alert = Alert.objects.get(pk=alert_id)
    except Alert.DoesNotExist:
        return JsonResponse({"detail": "Alert not found"}, status=404)

    return JsonResponse(
        {
            "alert_id": alert.id,
            "explanation": generate_explanation(alert),
            "generated_at": timezone.now(),
        }
    )
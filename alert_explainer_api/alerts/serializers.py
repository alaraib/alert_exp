from rest_framework import serializers


class AlertCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    severity = serializers.ChoiceField(choices=("critical", "warning", "info"))
    source = serializers.CharField()
    metric_name = serializers.CharField()
    metric_value = serializers.FloatField()
    threshold = serializers.FloatField()


class AlertSerializer(AlertCreateSerializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class ExplainResponseSerializer(serializers.Serializer):
    alert_id = serializers.IntegerField()
    explanation = serializers.CharField()
    generated_at = serializers.DateTimeField()
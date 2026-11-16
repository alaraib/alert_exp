import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Alert",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("critical", "Critical"),
                            ("warning", "Warning"),
                            ("info", "Info"),
                        ],
                        max_length=20,
                    ),
                ),
                ("source", models.CharField(max_length=255)),
                ("metric_name", models.CharField(max_length=255)),
                ("metric_value", models.FloatField()),
                ("threshold", models.FloatField()),
                (
                    "created_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={"db_table": "alerts"},
        ),
    ]
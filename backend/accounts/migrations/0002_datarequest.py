# Generated manually for J3-bis RGPD — audit trail SAR

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DataRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "request_type",
                    models.CharField(
                        choices=[
                            ("access", "Accès (art. 15)"),
                            ("export", "Export portabilité (art. 20)"),
                            ("deletion", "Effacement (art. 17)"),
                        ],
                        default="access",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("recue", "Reçue"),
                            ("en_cours", "En cours"),
                            ("repondue", "Répondue"),
                        ],
                        default="recue",
                        max_length=20,
                    ),
                ),
                (
                    "export_format",
                    models.CharField(
                        blank=True,
                        help_text="Format du fichier exporté (json, csv…).",
                        max_length=10,
                    ),
                ),
                (
                    "export_file_hash",
                    models.CharField(
                        blank=True,
                        help_text="Empreinte SHA-256 du fichier transmis (hex).",
                        max_length=64,
                    ),
                ),
                ("requested_at", models.DateTimeField(auto_now_add=True)),
                ("responded_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="data_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "demande d'accès aux données",
                "verbose_name_plural": "demandes d'accès aux données",
                "ordering": ["-requested_at"],
            },
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-03 23:19

import apps.territory.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("buildings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hotspot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("h", models.FloatField()),
                ("v", models.FloatField()),
                ("index", models.FloatField(blank=True, null=True)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotspots",
                        to="buildings.post",
                    ),
                ),
                (
                    "src",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="srcs",
                        to="buildings.post",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Territory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(upload_to=apps.territory.models.upload_panorama),
                ),
                (
                    "post",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="territories",
                        to="buildings.post",
                    ),
                ),
            ],
            options={
                "verbose_name": "территория",
                "verbose_name_plural": "территории",
            },
        ),
        migrations.CreateModel(
            name="TerritoryHotspot",
            fields=[
                (
                    "post",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="territory_hotspot",
                        serialize=False,
                        to="buildings.post",
                    ),
                ),
                ("h", models.FloatField()),
                ("v", models.FloatField()),
                ("index", models.FloatField(blank=True, null=True)),
                (
                    "territory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hotspots",
                        to="territory.territory",
                    ),
                ),
            ],
            options={
                "unique_together": {("post", "territory")},
            },
        ),
    ]

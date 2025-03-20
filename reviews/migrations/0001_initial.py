# Generated by Django 5.0.3 on 2025-03-18 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cafes", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("rating", models.DecimalField(decimal_places=1, max_digits=2)),
                ("comment", models.TextField(blank=True, null=True)),
                (
                    "cafe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cafes.cafeshop"
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.customer"
                    ),
                ),
            ],
            options={
                "db_table": "review",
            },
        ),
    ]

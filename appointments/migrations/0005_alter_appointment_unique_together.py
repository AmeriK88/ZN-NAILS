# Generated by Django 5.1.4 on 2025-01-15 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_appointment_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together=set(),
        ),
    ]

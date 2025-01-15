# Generated by Django 5.1.4 on 2025-01-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_appointment_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='comment',
            field=models.TextField(blank=True, help_text='Añade un comentario o instrucción especial', null=True),
        ),
    ]

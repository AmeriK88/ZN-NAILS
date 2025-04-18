# Generated by Django 5.1.5 on 2025-01-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='static/imagenes/')),
                ('disponible', models.BooleanField(default=True)),
                ('duracion', models.PositiveIntegerField(default=30, help_text='Duración del servicio en minutos')),
            ],
        ),
    ]

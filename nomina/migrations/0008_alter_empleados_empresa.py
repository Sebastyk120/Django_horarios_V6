# Generated by Django 4.2 on 2023-05-06 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomina', '0007_alter_opejornada_extras_nocturnos_totales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleados',
            name='empresa',
            field=models.CharField(choices=[('Heavens Fruits SAS', 'Heavens Fruits SAS'), ('People', 'People'), ('Turnos', 'Turnos')], default='Heavens Fruits SAS', max_length=100, verbose_name='Empresa'),
        ),
    ]

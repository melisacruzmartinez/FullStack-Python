# Generated by Django 3.1.3 on 2020-11-29 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0004_observacion_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observacion',
            name='Turno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinica.consulta'),
        ),
    ]
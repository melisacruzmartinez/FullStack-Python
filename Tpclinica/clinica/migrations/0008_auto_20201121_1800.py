# Generated by Django 3.1.2 on 2020-11-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica', '0007_auto_20201121_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='enfoque',
            field=models.CharField(blank=True, choices=[('L', 'Lejos'), ('C', 'Cerca')], max_length=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='lado',
            field=models.CharField(blank=True, choices=[('I', 'Izqierda'), ('D', 'Derecha')], max_length=1),
        ),
    ]

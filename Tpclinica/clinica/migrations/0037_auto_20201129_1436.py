# Generated by Django 3.1.2 on 2020-11-29 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        #('clinica', '0036_auto_20201129_0955'),
=======
        # ('clinica', '0036_auto_20201129_0955'),
>>>>>>> ac78071e725251e22c09de26d6f840b92ff93e33
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='tipo',
            field=models.CharField(choices=[('L', 'Lente'), ('E', 'Estuche'), ('G', 'Gotita'), ('A', 'Accesorios')], default='L', max_length=1),
        ),
    ]

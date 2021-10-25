# Generated by Django 3.2.8 on 2021-10-25 15:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20211025_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 9, 44, 52, 848763)),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 9, 44, 52, 848763)),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'player'), (2, 'sponsor'), (3, 'drinkMeister'), (4, 'manager')], default=1),
        ),
    ]
# Generated by Django 3.2.8 on 2021-10-25 15:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20211025_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 15, 46, 50, 23713, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 15, 46, 50, 23713, tzinfo=utc)),
        ),
    ]
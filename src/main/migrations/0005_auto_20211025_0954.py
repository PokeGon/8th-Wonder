# Generated by Django 3.2.8 on 2021-10-25 15:54

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20211025_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank',
            field=models.OneToOneField(default='BankAccount', on_delete=django.db.models.deletion.CASCADE, to='main.bankaccount'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 15, 54, 15, 28871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(default=datetime.datetime(2021, 10, 25, 15, 54, 15, 28871, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.IntegerField(default=1),
        ),
    ]

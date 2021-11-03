# Generated by Django 3.2.8 on 2021-11-02 23:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_manager_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkmeister',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='drinkmeister', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='player',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='player', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
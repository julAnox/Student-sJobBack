# Generated by Django 4.2.7 on 2023-11-13 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echoApp', '0009_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='place_of_education',
        ),
        migrations.AddField(
            model_name='user',
            name='place_of_education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='echoApp.education'),
        ),
    ]

# Generated by Django 4.1 on 2022-08-11 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_care_log_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animal',
            options={'ordering': ['species', 'name']},
        ),
    ]

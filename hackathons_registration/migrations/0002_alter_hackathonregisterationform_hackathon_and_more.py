# Generated by Django 5.0 on 2023-12-22 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon_template', '0015_alter_containerproperty_container'),
        ('hackathons_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathonregisterationform',
            name='hackathon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon_template.hackathon'),
        ),
        migrations.DeleteModel(
            name='Hackathon',
        ),
    ]

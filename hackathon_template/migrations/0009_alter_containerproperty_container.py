# Generated by Django 5.0 on 2023-12-18 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon_template', '0008_alter_textproperties_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='containerproperty',
            name='container',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hackathon_template.container'),
        ),
    ]
# Generated by Django 5.0 on 2023-12-20 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathon_template', '0011_alter_hackathon_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='organisation_name',
            field=models.CharField(default=None, max_length=250),
        ),
    ]

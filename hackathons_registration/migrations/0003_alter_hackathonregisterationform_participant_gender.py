# Generated by Django 5.0 on 2024-02-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathons_registration', '0002_remove_customfield_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackathonregisterationform',
            name='participant_gender',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
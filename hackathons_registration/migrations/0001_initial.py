# Generated by Django 5.0 on 2023-12-22 20:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hackathon_template', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('label', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Short', 'Short'), ('Long', 'Long'), ('Down', 'Down'), ('Multiple', 'Multiple')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DropdownField',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('choices', models.TextField()),
                ('custom_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hackathons_registration.customfield')),
            ],
        ),
        migrations.CreateModel(
            name='HackathonRegisterationForm',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('participant_name', models.CharField(blank=True, max_length=100)),
                ('participant_email', models.EmailField(blank=True, max_length=254)),
                ('participant_phone', models.IntegerField(null=True)),
                ('participant_gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('hackathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathon_template.hackathon')),
            ],
        ),
        migrations.AddField(
            model_name='customfield',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathons_registration.hackathonregisterationform'),
        ),
        migrations.CreateModel(
            name='LongAnswerField',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=1000)),
                ('custom_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hackathons_registration.customfield')),
            ],
        ),
        migrations.CreateModel(
            name='MultipleChoiceField',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('option', models.CharField(max_length=500)),
                ('custom_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hackathons_registration.customfield')),
            ],
        ),
        migrations.CreateModel(
            name='ShortAnswerField',
            fields=[
                ('_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=500)),
                ('custom_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hackathons_registration.customfield')),
            ],
        ),
    ]

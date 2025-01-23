# Generated by Django 5.0.6 on 2024-10-31 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_jobrequirements_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_requirements', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobrequirements')),
                ('jobprovider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobproviderregister')),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.jobseekerregister')),
            ],
        ),
    ]

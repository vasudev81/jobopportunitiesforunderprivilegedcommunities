# Generated by Django 5.1.4 on 2025-01-17 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0016_remove_exam_exam_log_remove_exam_exam_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumes',
            name='resume_file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]

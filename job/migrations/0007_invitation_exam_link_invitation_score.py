# Generated by Django 5.0.6 on 2024-11-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='exam_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

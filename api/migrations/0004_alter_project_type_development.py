# Generated by Django 3.2.20 on 2023-08-05 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_type_project_type_development'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type_development',
            field=models.CharField(choices=[('BACKEND', 'BACKEND'), ('FRONTEND', 'FRONTEND'), ('IOS', 'IOS'), ('ANDROID', 'ANDROID')], max_length=12),
        ),
    ]

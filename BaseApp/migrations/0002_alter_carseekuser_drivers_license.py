# Generated by Django 4.2.10 on 2024-03-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carseekuser',
            name='drivers_license',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
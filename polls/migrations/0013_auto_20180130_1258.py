# Generated by Django 2.0.1 on 2018-01-30 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_auto_20180130_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformations',
            name='postalCode',
            field=models.CharField(max_length=7),
        ),
    ]
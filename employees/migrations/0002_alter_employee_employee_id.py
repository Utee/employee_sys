# Generated by Django 5.0.6 on 2024-11-01 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]

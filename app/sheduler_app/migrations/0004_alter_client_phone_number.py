# Generated by Django 4.1.3 on 2022-12-11 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheduler_app', '0003_alter_operatorcode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='phone_number',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
# Generated by Django 3.1.2 on 2020-10-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20201004_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.FileField(upload_to=''),
        ),
    ]

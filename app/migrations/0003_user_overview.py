# Generated by Django 2.1 on 2018-09-30 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180927_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='overview',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

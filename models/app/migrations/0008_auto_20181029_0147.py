# Generated by Django 2.1 on 2018-10-29 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20181001_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.TextField(default='foo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='salt',
            field=models.CharField(default='bar', max_length=19),
            preserve_default=False,
        ),
    ]
# Generated by Django 4.1 on 2022-09-17 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 17, 21, 35, 35, 347018, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]

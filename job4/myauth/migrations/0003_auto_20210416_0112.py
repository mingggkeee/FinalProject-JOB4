# Generated by Django 3.1.7 on 2021-04-16 01:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0002_auto_20210416_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]

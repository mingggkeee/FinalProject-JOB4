# Generated by Django 3.1.7 on 2021-04-16 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('user', 'letter')},
        ),
    ]

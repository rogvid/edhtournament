# Generated by Django 3.0.8 on 2020-10-05 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together={('tournament', 'person')},
        ),
    ]

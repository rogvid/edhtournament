# Generated by Django 3.0.8 on 2020-08-02 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]

# Generated by Django 3.0.8 on 2020-10-07 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0009_auto_20201007_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Participant'),
        ),
        migrations.AlterField(
            model_name='player',
            name='pod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pod_players', to='tournament.Pod'),
        ),
    ]
# Generated by Django 3.0.8 on 2020-10-05 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standing', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=90)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.IntegerField(blank=True, null=True)),
                ('won', models.BooleanField(blank=True, null=True)),
                ('draw', models.BooleanField(blank=True, null=True)),
                ('deck', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Deck')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('winscore', models.IntegerField(default=3)),
                ('drawscore', models.IntegerField(default=1)),
                ('losescore', models.IntegerField(default=0)),
                ('max_rounds', models.IntegerField(blank=True, default=3, null=True)),
                ('max_round_duration', models.DurationField(blank=True, default=3600, null=True)),
                ('tournament_players', models.ManyToManyField(through='tournament.Participant', to='tournament.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Pod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('pod_players', models.ManyToManyField(through='tournament.Player', to='tournament.Person')),
                ('tournament', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='pod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Pod'),
        ),
        migrations.AddField(
            model_name='participant',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Person'),
        ),
        migrations.AddField(
            model_name='participant',
            name='tournament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('pod', 'person')},
        ),
    ]

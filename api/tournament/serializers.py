# serializers.py

from rest_framework import serializers

from .models import Player, Pod, Tournament


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('first_name', 'last_name')

class TournamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'created_at', 'finished_at', 'tournament_players', 'winscore', 'drawscore', 'losescore')

class PodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pod
        fields = ('pod_players', 'created_at', 'duration', 'finished_at', 'winner', 'tournament')

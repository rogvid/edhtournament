# views.py

from rest_framework import viewsets

from .models import Player, Pod, Tournament
from .serializers import PlayerSerializer, PodSerializer, TournamentSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PodViewSet(viewsets.ModelViewSet):
    queryset = Pod.objects.all()
    serializer_class = PodSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

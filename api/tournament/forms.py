from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.mixins import CreateUpdateAjaxMixin, PopRequestMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Participant, Person, Player, Pod, Tournament


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class TournamentModelForm(BSModalModelForm):
    class Meta:
        model = Tournament
        fields = [
            "name", "admin", "winscore", "drawscore", "losescore",
            "max_rounds", "max_round_duration", "max_pod_players",
            "min_pod_players"
        ]


class ParticipantModelForm(BSModalModelForm):
    class Meta:
        model = Participant
        fields = ["person", "tournament"]


class PersonModelForm(BSModalModelForm):
    class Meta:
        model = Person
        fields = ["name"]


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

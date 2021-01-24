import datetime
import random

import numpy as np
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalDeleteView, BSModalLoginView,
                                           BSModalUpdateView)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import (CustomAuthenticationForm, CustomUserCreationForm,
                    ParticipantModelForm, PersonModelForm, TournamentModelForm)
from .models import Participant, Person, Player, Pod, Tournament


class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('tournaments')


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy("home"))


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'forms/login.html'
    success_message = 'Success: You were successfully logged in.'
    extra_context = dict(success_url=reverse_lazy('tournaments'))


class Index(View):
    template = 'index.html'

    def get(self, request):
        return render(request, self.template)


class Tournaments(LoginRequiredMixin, View):
    template = "tournaments.html"
    login_url = "login"

    # success_url

    def get(self, request):
        tournaments = Tournament.objects.all()
        pods = Pod.objects.all()
        players = Player.objects.all()
        return render(request, self.template, {'tournaments': tournaments})


def view_tournament(request, pk):
    participants = Participant.objects.filter(
        tournament__pk=pk).order_by('-score')
    pods = Pod.objects.filter(
        tournament__pk=pk).prefetch_related('pod_players').order_by('-pk')
    tournament = Tournament.objects.get(pk=pk)
    # players = Player.objects.filter(pod=pods)
    return render(request, "tournament.html", {
        "participants": participants,
        "pods": pods,
        "tournament": tournament,
    })


def make_change(coins: list, change: int):
    """"""
    coins_used = [0] * (change + 1)
    min_coins = [1] + [0] * (change)

    for i in range(len(min_coins)):
        n = 0
        for j in range(len(coins)):
            if coins[j] <= i:
                min_coins[i] += min_coins[i - coins[j]]
                n = coins[j]
        coins_used[i] = n

    return min_coins[change], coins_used


def get_change(coins_used, change, max_iterations=1000):
    coins = []
    coin = change
    iterations = 0
    while coin > 0:
        coins.append(coins_used[coin])
        coin = coin - coins_used[coin]
        iterations += 1
        if iterations > max_iterations:
            break
    return coins


def make_pod_sizes(sizes, n_players):
    min_pods, pod_sizes = make_change(sizes, n_players)

    if min_pods != 0:
        pods = get_change(pod_sizes, n_players)
        return pods
    else:
        return []


def new_round(request, *args, **kwargs):
    tournament_id = kwargs["tournament_id"]
    pods = Pod.objects.filter(tournament__pk=tournament_id)
    if (len(pods.filter(finished_at__isnull=True)) == 0) or (len(pods) == 0):
        # TODO: Get tournament pod generation rules
        # The rules should be something along the line of:
        # 1. sort by points (default)
        # 2. diversify (least amount of players who have played each other)
        # 3. random
        print("Update player scores")
        update_participant_scores(tournament_id)
        print("Getting participants")
        participants = list(
            Participant.objects.filter(tournament__pk=tournament_id).order_by(
                "-score", "-ogw"))
        # Get tournament rules
        print("Getting tournaments")
        tournament = Tournament.objects.get(pk=tournament_id)
        pod_sizes = list(
            range(tournament.min_pod_players, tournament.max_pod_players + 1))
        print("Making pod sizes")
        print(pod_sizes)
        print(participants)
        S = make_pod_sizes(pod_sizes, len(participants))

        if len(pods) == 0:
            round_nr = 1
        else:
            round_nr = pods.order_by("-round_nr")[0].round_nr + 1

        for pod_size in S:
            print("Creating new pods")
            new_pod = Pod(tournament=tournament, round_nr=round_nr)
            new_pod.save()
            seats = list(range(1, pod_size + 1))
            random.shuffle(seats)
            for i in range(pod_size):
                seat = seats[i]
                pod_participant = Player(pod=new_pod,
                                         participant=participants.pop(),
                                         seat=seat)
                pod_participant.save()

    return HttpResponseRedirect(
        reverse_lazy("tournament", kwargs={"pk": tournament_id}))


class TournamentCreateView(BSModalCreateView):
    template_name = 'forms/create_tournament.html'
    model = Tournament
    form_class = TournamentModelForm
    success_message = 'Success: Tournament was created'
    success_url = reverse_lazy('tournaments')


class TournamentUpdateView(BSModalUpdateView):
    template_name = 'forms/update_tournament.html'
    model = Tournament
    form_class = TournamentModelForm
    success_message = 'Success: Tournament was updated'
    success_url = reverse_lazy('tournaments')


class TournamentDeleteView(BSModalDeleteView):
    template_name = 'forms/delete_tournament.html'
    model = Tournament
    form_class = TournamentModelForm
    success_message = 'Success: Tournament was delete'
    success_url = reverse_lazy('tournaments')


class ParticipantCreateView(BSModalCreateView):
    template_name = 'forms/create_participant.html'
    model = Person
    form_class = PersonModelForm

    def post(self, request, *args, **kwargs):
        pk = kwargs["tournament_id"]
        form = self.form_class(request.POST)
        form_error = True
        if form.is_valid():
            name = form.cleaned_data.get("name")
            if not Participant.objects.filter(person__name=name,
                                              tournament__pk=pk):
                tournament = Tournament.objects.get(pk=pk)
                person = Person(name=name)
                person.save()
                participant = Participant(tournament=tournament, person=person)
                participant.save()
        return HttpResponseRedirect(
            reverse_lazy("tournament", kwargs={"pk": pk}))


class ParticipantUpdateView(BSModalUpdateView):
    template_name = 'forms/update_participant.html'
    model = Participant
    form_class = PersonModelForm
    success_message = 'Success: Tournament was delete'

    def post(self, request, *args, **kwargs):
        tournament_id = kwargs["tournament_id"]
        pk = kwargs["pk"]
        form = self.form_class(request.POST)
        form_error = True
        if form.is_valid():
            new_name = form.cleaned_data.get("name")
            if not Participant.objects.filter(person__name=new_name):
                old_name = Participant.objects.get(pk=pk).person.name
                person = Person.objects.get(name=old_name)
                person.name = new_name
                person.save()
        return HttpResponseRedirect(
            reverse_lazy("tournament", kwargs={"pk": tournament_id}))


class ParticipantDeleteView(BSModalDeleteView):
    template_name = 'forms/delete_participant.html'
    model = Participant
    form_class = ParticipantModelForm
    success_message = 'Success: Tournament was delete'

    def post(self, request, *args, **kwargs):
        tournament_id = kwargs["tournament_id"]
        pk = kwargs["pk"]
        form = self.form_class(request.POST)
        form_error = True
        Participant.objects.filter(pk=pk).delete()
        print("HERE")
        return HttpResponseRedirect(
            reverse_lazy("tournament", kwargs={"pk": tournament_id}))


def ogw(participant_id, pods):
    gws = []
    for pod in pods:
        pod_players = Player.objects.filter(pod=pod.pk)
        for player in pod_players:
            if player.participant.pk != participant_id:
                gws.append(player.participant.gw)
    score = np.mean(gws)
    if score < 12.5:
        return 12.5
    return score


def update_participant_scores(tournament_id):
    participants = Participant.objects.filter(tournament=tournament_id)
    # We start by updateing their scores
    for participant in participants:
        games_played = Player.objects.filter(participant=participant.pk)
        participant.gw = len(games_played.filter(won=True)) / np.max(
            [len(games_played), 1]) * 100.0
        participant.save()

    # We then update their OGW
    for participant in participants:
        pods = Pod.objects.filter(pod_players__participant=participant.pk)
        participant.ogw = ogw(participant.pk, pods)
        participant.save()


def set_pod_winner(request, *args, **kwargs):
    pod_id = kwargs["pk"]
    player_id = kwargs["player_id"]
    tournament_id = kwargs["tournament_id"]

    Player.objects.filter(pk=player_id).update(won=True)
    Pod.objects.filter(pk=pod_id).update(finished_at=datetime.datetime.now())
    participant = Player.objects.get(pk=player_id).participant
    participant.score += Tournament.objects.get(pk=tournament_id).winscore
    participant.save()
    update_participant_scores(tournament_id)
    return HttpResponseRedirect(
        reverse_lazy("tournament", kwargs={"pk": tournament_id}))


def update_pod(request, *args, **kwargs):
    pk = kwargs["pk"]
    pod = Pod.objects.get(pk=pk)
    tournament_id = kwargs["tournament_id"]
    PlayerInlineFormset = inlineformset_factory(Pod,
                                                Player,
                                                fields=("participant", "deck",
                                                        "won"),
                                                can_delete=False)
    if request.POST:
        formset = PlayerInlineFormset(request.POST, instance=pod)
        print
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(
                reverse_lazy("tournament", kwargs={"pk": tournament_id}))
    else:
        formset = PlayerInlineFormset(instance=pod)
        print(formset)
    return render(request, "forms/update_pod.html", {"formset": formset})

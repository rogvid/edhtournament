from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

#app_name = "tournament"

urlpatterns = [
    path("", views.Index.as_view(), name='home'),
    # Tournament
    path("tournaments/", views.Tournaments.as_view(), name="tournaments"),
    path("tournaments/<int:pk>/", views.view_tournament, name="tournament"),
    path("tournaments/create",
         views.TournamentCreateView.as_view(),
         name="create_tournament"),
    path("tournaments/<int:pk>/update",
         views.TournamentUpdateView.as_view(),
         name="update_tournament"),
    path("tournaments/<int:pk>/delete",
         views.TournamentDeleteView.as_view(),
         name="delete_tournament"),
    # Participants
    path("tournaments/<int:tournament_id>/participants/create",
         views.ParticipantCreateView.as_view(),
         name="create_participant"),
    path("tournaments/<int:tournament_id>/participants/<int:pk>/delete",
         views.ParticipantDeleteView.as_view(),
         name="delete_participant"),
    path("tournaments/<int:tournament_id>/participants/<int:pk>/update",
         views.ParticipantUpdateView.as_view(),
         name="update_participant"),
    # Rounds
    path("tournaments/<int:tournament_id>/rounds/create",
         views.new_round,
         name="create_round"),
    # Pods
    path("tournaments/<int:tournament_id>/pods/<int:pk>/update",
         views.update_pod,
         name="update_pod"),
    path(
        "tournaments/<int:tournament_id>/pods/<int:pk>/winner/<int:player_id>",
        views.set_pod_winner,
        name="set_pod_winner")
]

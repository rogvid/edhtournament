from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    """Person class."""

    name = models.CharField(max_length=90)

    def __str__(self):
        return self.name


class Deck(models.Model):
    """Deck class."""

    name = models.CharField(max_length=90)


class Tournament(models.Model):
    """Tournament class."""

    name = models.CharField(max_length=200)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: Check how to correctly add an end time
    finished_at = models.DateTimeField(blank=True, null=True)
    tournament_players = models.ManyToManyField(Person, through="Participant")
    winscore = models.IntegerField(default=3)
    drawscore = models.IntegerField(default=1)
    losescore = models.IntegerField(default=0)
    max_rounds = models.IntegerField(default=3, blank=True, null=True)
    # TODO: Check how default for durationfields work (milliseconds or seconds)
    max_round_duration = models.DurationField(default=60 * 60,
                                              blank=True,
                                              null=True)
    max_pod_players = models.IntegerField(default=4, blank=True, null=True)
    min_pod_players = models.IntegerField(default=3, blank=True, null=True)

    def __str__(self):  # noqa
        return str(self.name)


class Participant(models.Model):
    """Participant class."""

    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   blank=True,
                                   null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, blank=True, null=True)
    gw = models.FloatField(default=0, blank=True, null=True)
    ogw = models.FloatField(default=0, blank=True, null=True)

    # elo = models.FloatField(default=400, blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.tournament.name, self.person.name)

    class Meta:
        """Meta information."""

        unique_together = [
            ("tournament", "person"),
        ]


class Pod(models.Model):
    """Pod class."""

    # TODO: Change this to be dependent on tournament players
    tournament = models.ForeignKey(Tournament,
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    round_nr = models.IntegerField(default=1)

    def winner(self):
        try:
            p = self.pod_players.get(won=True)
        except:
            p = None
        return p


class Player(models.Model):
    """Player class."""

    pod = models.ForeignKey(Pod,
                            on_delete=models.CASCADE,
                            related_name="pod_players")
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    deck = models.ForeignKey(Deck,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    seat = models.IntegerField(blank=True, null=True)
    won = models.BooleanField(default=False)
    draw = models.BooleanField(default=False)

    def name(self):
        return self.participant.person.name

    class Meta:
        """Meta information."""

        unique_together = [
            ("pod", "participant"),
        ]

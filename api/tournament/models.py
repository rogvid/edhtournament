from django.db import models


# Create your models here.
class Player(models.Model):
    """Player class"""
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    # TODO: Add image of player (if desired)

    def __str__(self):
        return " ".join(
            str(s) for s in [
                self.first_name,
                self.last_name
            ]
            if s is not None
        )

class Format(models.Model):
    """Tournament Format Class"""
    name = models.CharField(max_length=300)
    # TODO: Add tournament format description and rules


class Tournament(models.Model):
    """Tournament class"""
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: Check how to correctly add an end time
    finished_at = models.DateTimeField(auto_now_add=True)
    tournament_players = models.ManyToManyField(
        Player,
        related_name="+"
    )
    winscore = models.IntegerField(default=3)
    drawscore = models.IntegerField(default=1)
    losescore = models.IntegerField(default=0)
    max_rounds = models.IntegerField(default=3, blank=True, null=True)
    # TODO: Check how default for durationfields work (milliseconds or seconds)
    max_round_duration = models.DurationField(default=60*60, blank=True, null=True)
    tournament_format = models.ForeignKey(
        Format,
        related_name="+",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)


class Pod(models.Model):
    """Pod class"""
    # TODO: Change this to be dependent on tournament players
    pod_players = models.ManyToManyField(
        Player, related_name="+"
    )
    tournament_round = models.IntegerField(default=1)
    # TODO: Make this dependent on tournament players not players in general
    winner = models.ForeignKey(
        Player,
        related_name="pod_winner",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    duration = models.DurationField(default=0)
    tournament = models.ForeignKey(Tournament, related_name="+", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: Check how to correctly add an end time
    finished_at = models.DateTimeField()


    def __str__(self):
        # TODO: Modify so the return name is tournament name, tournament round, and pod number
        return """
        {0} Round {1}
        """.format(
            self.tournament.name,
            self.tournament_round
        )

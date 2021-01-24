from django.contrib import admin

from .models import Participant, Person, Player, Pod, Tournament

# Register your models here.
admin.site.register(Person)
admin.site.register(Tournament)
admin.site.register(Participant)
admin.site.register(Pod)
admin.site.register(Player)

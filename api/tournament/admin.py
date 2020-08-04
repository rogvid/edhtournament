from django.contrib import admin

from .models import Player, Pod, Tournament

# Register your models here.
admin.site.register(Player)
admin.site.register(Pod)
admin.site.register(Tournament)

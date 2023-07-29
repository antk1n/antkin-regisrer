from django.contrib import admin

# Register your models here.

from .models import Osauhing, Isikud, Osauhing_Isikud

admin.site.register(Osauhing)
admin.site.register(Osauhing_Isikud)
admin.site.register(Isikud)
from django.contrib import admin

# Register your models here.
from .models import Song, Leader

admin.site.register(Song)
admin.site.register(Leader)
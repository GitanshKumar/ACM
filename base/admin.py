from django.contrib import admin
from .models import Event, Member, Photo, Student, Team, Tag, News, Byte

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_date', 'incharge']

@admin.register(Member)
class CoorAdmin(admin.ModelAdmin):
    list_display = ['name', 'core']

@admin.register(Team)
class CoorAdmin(admin.ModelAdmin):
    readonly_fields = ('team_id',)

admin.site.register((Photo, Student, Tag, News, Byte))
from django.contrib import admin

from .models import MyClubUser, Event

# Register your models here.


admin.site.register(MyClubUser)


class EventAdmin(admin.ModelAdmin):
	list_display = ['name', 'event_date', 'venue', 'manager']
	fields = [('name', 'venue'), 'event_date', 'manager', 'description', 'approved']
	list_filter = ['name', 'event_date', 'approved']
	ordering = ['-event_date',]

admin.site.register(Event, EventAdmin)
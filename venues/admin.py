from django.contrib import admin

from .models import Venue

# Register your models here.





class VenueAdmin(admin.ModelAdmin):
	list_display = ['name', 'address', 'phone']
	ordering = ['name',]
	search_fields = ['name', 'address', 'email', 'phone']

admin.site.register(Venue, VenueAdmin)
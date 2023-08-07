from django.db import models
from django.contrib.auth.models import User
from datetime import date

from venues.models import Venue

# Create your models here.


class MyClubUser(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()

	def __str__(self):
		return f'{self.first_name} {self.last_name}'



class Event(models.Model):
	name = models.CharField(max_length=120)
	event_date = models.DateTimeField()
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(User, blank=True)
	approved = models.BooleanField(default=False)
	

	def __str__(self):
		return self.name


	@property
	def days_till_event(self):
		today = date.today()
		days_till = self.event_date.date() - today
		days_till_stripped = str(days_till).split(',', 1)[0]

		if days_till_stripped[0] == '-' :
			days_till_stripped = f"It's over {days_till_stripped[1:]} back"

			return days_till_stripped
		
		return days_till_stripped
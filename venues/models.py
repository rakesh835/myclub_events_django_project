from django.db import models

# Create your models here.

class Venue(models.Model):
	name = models.CharField(max_length=120)
	address = models.CharField(max_length=300)
	pin_code = models.CharField(max_length=6)
	phone = models.CharField(max_length=15)
	web_address = models.URLField()
	email = models.EmailField()
	owner = models.IntegerField(blank=False, default=1)
	venue_image = models.ImageField(null=True, blank=True, upload_to='images/venues/')


	def __str__(self):
		return self.name
from django import forms

from .models import Venue


class VenueForm(forms.ModelForm):

	class Meta:
		model = Venue
		fields = ['name', 'address', 'pin_code', 'phone', 'web_address', 'email', 'venue_image']

	
	def __init__(self, *args, **kwargs):
		super(VenueForm, self).__init__(*args, **kwargs)

		self.fields['name'].widget.attrs['placeholder'] = 'Venue Name'
		self.fields['address'].widget.attrs['placeholder'] = 'Address'
		self.fields['pin_code'].widget.attrs['placeholder'] = 'Pin Code'
		self.fields['phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
		self.fields['web_address'].widget.attrs['placeholder'] = 'Enter Website address'
		self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'

		for field in self.fields:
			self.fields[field].widget.attrs['class'] = 'form-control'



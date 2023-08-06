from django import forms

from .models import Event


class EventFormAdmin(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['name', 'event_date', 'venue', 'manager', 'description', 'attendees']

	
	def __init__(self, *args, **kwargs):
		super(EventFormAdmin, self).__init__(*args, **kwargs)

		self.fields['name'].widget.attrs['placeholder'] = 'Event Name'
		self.fields['event_date'].widget.attrs['placeholder'] = 'Event Date'
		self.fields['description'].widget.attrs['placeholder'] = 'Write description'
		self.fields['attendees'].widget.attrs['placeholder'] = 'Attendees'


		self.fields['name'].widget.attrs['class'] = 'form-control'
		self.fields['attendees'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['class'] = 'form-control'

		self.fields['venue'].widget.attrs = {'class': 'form-select', 'placeholder': 'Select venue'}
		self.fields['manager'].widget.attrs = {'class': 'form-select', 'placeholder': 'Select manager'}
		self.fields['event_date'].widget.attrs = {'class': 'form-control'}



class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['name', 'event_date', 'venue', 'description', 'attendees']

	
	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)

		self.fields['name'].widget.attrs['placeholder'] = 'Event Name'
		self.fields['event_date'].widget.attrs['placeholder'] = 'Event Date'
		self.fields['description'].widget.attrs['placeholder'] = 'Write description'
		self.fields['attendees'].widget.attrs['placeholder'] = 'Attendees'


		self.fields['name'].widget.attrs['class'] = 'form-control'
		self.fields['attendees'].widget.attrs['class'] = 'form-control'
		self.fields['description'].widget.attrs['class'] = 'form-control'

		self.fields['venue'].widget.attrs = {'class': 'form-select', 'placeholder': 'Select venue'}
		self.fields['event_date'].widget.attrs = {'class': 'form-control'}
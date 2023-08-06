from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Event
from .forms import EventForm, EventFormAdmin
from venues.models import Venue

# Create your views here.


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create a calendar
	cal = HTMLCalendar().formatmonth(year, month_number)

	# Get current year
	now = datetime.now()
	current_year = now.year
	
	# Query the event model by date
	event_list = Event.objects.filter(
						event_date__year=year,
						event_date__month=month_number)

	context = {
			'year': year,
			'month': month,
			'cal': cal,
			'event_list': event_list,
	}

	return render(request, 'events/home.html', context)



@login_required
def events_list(request):
	events = Event.objects.all().filter(approved=True).order_by('-event_date')
	paginator = Paginator(events, 1)

	page_number = request.GET.get('page', 0)
	page_obj = paginator.get_page(page_number)

	context = {
		'events': page_obj,
	}

	return render(request, 'events/events_list.html', context)




@login_required
def event_detail(request, id):
	event = Event.objects.get(pk=id)
	
	context = {
		'event': event,
	}
	print("event: ", event.attendees)
	return render(request, 'events/event_detail.html', context)




@login_required
def add_event(request):
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None)
		
		if request.method == 'POST':

			if form.is_valid():
				form.save()

				return redirect('events_list')
	else:
		form = EventForm(request.POST or None)

		if request.method == 'POST':

			if form.is_valid():
				event = form.save(commit=False)
				event.manager = request.user
				event.save()

				return redirect('events_list')

	context = {
		'form': form, 
	}
	
	return render(request, 'events/add_event.html', context)



@login_required
def update_event(request, id):
	event = Event.objects.get(id=id)
	user = request.user

	if not user.is_superuser and not user == event.manager:
		messages.warning(request, 'You are not allowed to update this event.')
		return redirect('events_list')

	form = EventFormAdmin(request.POST or None, instance=event)

	if request.method == "POST":

		if form.is_valid():
			form.save()

			return redirect('events_list')

	context = {
		'form': form,
	}

	return render(request, 'events/update_event.html', context)



@login_required
def delete_event(request, id):
	event = Event.objects.get(id=id)

	if not user.is_superuser and not user == event.manager:
		messages.warning(request, 'You are not allowed to delete this event.')
		return redirect('events_list')

	event.delete()

	return redirect('events_list')



@login_required
def my_events(request):
	events = Event.objects.filter(attendees=request.user.id)
	paginator = Paginator(events, 1)

	page_number = request.GET.get('page', 0)
	page_obj = paginator.get_page(page_number)

	context={
		'events': page_obj,
	}

	return render(request, 'events/my_events.html', context)



def search_events(request):

	if request.method == 'GET':
		keyword = request.GET.get('keyword')

		if keyword:
			events = Event.objects.filter(Q(name__icontains=keyword) | Q(venue__name__icontains=keyword) | Q(description__icontains=keyword))

		else:
			events = None

	context = {
		'events': events,
	}

	return render(request, 'events/search_events.html', context)




def admin_approval(request):
	events = Event.objects.all().order_by('-event_date')
	event_count = events.count()

	venues = Venue.objects.all()
	venue_count = venues.count()
	
	user_count = User.objects.all().count()

	if request.user.is_superuser:
		if request.method == 'POST':
			id_list = request.POST.getlist('boxes')

			events.update(approved=False)

			for x in id_list:
				Event.objects.filter(pk=x).update(approved=True)

			messages.success(request, 'Event approval has been updated.')
			return redirect('events_list')

		else:
			context = {
				'events': events,
				'venues': venues,
				'event_count': event_count,
				'venue_count': venue_count,
				'user_count': user_count,
				}

			return render(request, 'events/admin_approval.html', context)

	else:
		messages.warning(request, 'You are not allowed to visit this page.')
		return redirect('home')



def show_events_by_venue(request, id):
	venue = Venue.objects.get(pk=id)
	events = Event.objects.filter(venue=venue)

	context = {
		'events': events,
		'venue': venue,
	}

	return render(request, 'events/show_events_by_venue.html', context)

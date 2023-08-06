from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Venue
from .forms import VenueForm
from events.models import Event

# Create your views here.


@login_required
def add_venue(request):
	form = VenueForm(request.POST or None, request.FILES or None)

	if request.method == 'POST':

		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id
			venue.save()

			return redirect('venue_list')
	
	context = {
		'form': form,
	}

	return render(request, 'venues/add_venue.html', context)




def venue_list(request):
	venues = Venue.objects.all().order_by('name')
	paginator = Paginator(venues, 1)

	page_number = request.GET.get('page', 0)
	page_obj = paginator.get_page(page_number)

	
	context = {
		'venues': page_obj,
	}

	return render(request, 'venues/venue_list.html', context)



@login_required
def venue_detail(request, id):
	venue = Venue.objects.get(id=id)
	venue_owner = User.objects.get(id=venue.owner)

	events = Event.objects.filter(venue=venue)

	context = {
		'venue': venue,
		'venue_owner': venue_owner,
		'events': events,
	}

	return render(request, 'venues/venue_detail.html', context)



def serach_venues(request):

	if request.GET:
		keyword = request.GET.get('keyword')

		if keyword:
			venues = Venue.objects.filter(Q(name__icontains=keyword) | Q(address__icontains=keyword) | Q(pin_code__icontains=keyword))
		else:
			keyword = ''
			venues = None

	context = {
		'venues': venues,
		'query': str(keyword),
	}

	return render(request, 'venues/search_venues.html', context)



@login_required
def update_venue(request, id):
	venue = Venue.objects.get(pk=id)
	user = request.user

	if not user.is_superuser and not request.user.id == venue.owner:
		messages.warning(request, 'You are not allowed to update this venue.')
		return redirect('venue_list')

	form = VenueForm(request.POST or None, request.FILES or None, instance=venue)

	if request.method == 'POST':
		
		if form.is_valid():
			form.save()

			return redirect('venue_list')


	context = {
		'form': form,
		'id': id,
	}

	return render(request, 'venues/update_venue.html', context)



@login_required
def delete_venue(request, id):
	venue = Venue.objects.get(id=id)
	user = request.user

	if not user.is_superuser and not request.user.id == venue.owner:
		messages.warning(request, 'You are not allowed to update this venue.')
		return redirect('venue_list')
	
	venue.delete()

	return redirect('venue_list')



@login_required
def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content_Disposition'] = 'attachment; filename=venues.txt'

	venues = Venue.objects.all()

	lines = []

	for venue in venues:
		lines.append(f'{venue.name}\n{venue.address}\n{venue.pin_code}\n{venue.phone}\n{venue.web_address}\n{venue.email}\n\n\n')


	response.writelines(lines)
	return response



@login_required
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content_Disposition'] = 'attachment; filename=venues.csv'

	# CSV writer
	writer = csv.writer(response)

	venues = Venue.objects.all()

	writer.writerow(['venue name', 'Address', 'Pin code', 'Phone', 'Web address', 'Email'])


	lines = []

	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.pin_code, venue.phone, venue.web_address, venue.email])

	return response



@login_required
def venue_pdf(request):
	# create Bytestream buffer 
	buf = io.BytesIO()
	#create canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# create text object
	textobj = c.beginText()
	textobj.setTextOrigin(inch, inch)
	textobj.setFont('Helvetica', 14)

	venues = Venue.objects.all()

	lines = []
	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.pin_code)
		lines.append(venue.phone)
		lines.append(venue.web_address)
		lines.append(venue.email)
		lines.append('  ')


	for line in lines:
		textobj.textLine(line)

	c.drawText(textobj)
	c.showPage()
	c.save()
	buf.seek(0)


	return FileResponse(buf, as_attachment=True, filename='venues.pdf')

from django.urls import path

from .views import (add_venue, venue_list, venue_detail,
					 serach_venues, update_venue, delete_venue,
                     venue_text, venue_csv, venue_pdf
                )


urlpatterns = [
	path('', venue_list, name='venue_list'),
    path('add_venue/', add_venue, name='add_venue'),
    path('venue_detail/<int:id>/', venue_detail, name='venue_detail'),
    path('search_venues/', serach_venues, name='search_venues'),
    path('update_venue/<int:id>/', update_venue, name='update_venue'),
    path('delete_venue/<int:id>/', delete_venue, name='delete_venue'),
    path('venue_text/', venue_text, name='venue_text'),
    path('venue_csv/', venue_csv, name='venue_csv'),
    path('venue_pdf/', venue_pdf, name='venue_pdf'),
    
    ]
from django.urls import path

from .views import (home, events_list, add_event, update_event,
                    delete_event, event_detail, my_events,
                    search_events, admin_approval, show_events_by_venue
    )
                


urlpatterns = [
    path('', home, name='home'),
    path('<int:year>/<str:month>/', home, name='dynamic_home'),
    path('events/', events_list, name='events_list'),
    path('add_event/', add_event, name='add_event'),
    path('update_event/<int:id>/', update_event, name='update_event'),
    path('delete_event/<int:id>/', delete_event, name='delete_event'),
    path('event_detail/<int:id>/', event_detail, name='event_detail'),
    path('my_events/', my_events, name='my_events'),
    path('search_events/', search_events, name='search_events'),
    path('admin_approval/', admin_approval, name='admin_approval'),
    path('show_events_by_venue/<int:id>/', show_events_by_venue, name='show_events_by_venue'),






]
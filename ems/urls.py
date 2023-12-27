from ems.views import selection
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import register_for_event
from . import views

urlpatterns = [
    path('register_participant/', views.registerPage, name='register_participant'),
    path('register_organiser/', views.registerPageOrganiser, name='register_organiser'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('selection/', views.selection, name='selection'),

    path('', views.home, name='home'),
    path('users/', views.users, name='participants'),
    path('user/<str:pk>', views.view_user, name='user'),
    path('organisers/', views.organisers, name='organisers'),
    path('events/', views.events, name='events'),
    path('my_events/', views.my_events, name='my_events'),
    path('register_for_event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('shippers/', views.shippers, name='shippers'),
    path('store/', views.store, name='store'),
    path('transactions/', views.transactions, name='transactions'),
    path('registrations/', views.registrations, name='registrations'),
    path('shipments/', views.shipments, name='shipments'),
    path('shippers/', views.shippers, name='shippers'),

    path('create_event/<str:pk>', views.createEvent, name='create_event'),
    path('add_item/<str:pk>', views.createItem, name='add_item'),
    path('add_organiser/', views.createOrganiser, name='add_organiser'),
    path('create_transaction/<str:pk>', views.createTransaction, name='create_transaction'),
    path('create_shipper/', views.createShipper, name='create_shipper'),
    path('create_registration/<str:pk>', views.createRegistration, name='create_registration'),
    path('create_shipment/<str:pk>', views.createShipment, name='create_shipment'),

    path('view_event/<str:pk>', views.view_event, name='view_event'),
    path('edit_profile_participant/<str:pk>', views.editProfileParticipant, name='edit_profile_participant'),
    path('edit_profile_organiser/<str:pk>', views.editProfileOrganiser, name='edit_profile_organiser'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
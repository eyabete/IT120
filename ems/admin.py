from django.contrib import admin
from .models import *


class OrganiserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name'
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name'
    )

admin.site.register(Participant)
admin.site.register(Organiser, OrganiserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Transaction)
admin.site.register(Cancellation)
admin.site.register(Item)
admin.site.register(Shipper)
admin.site.register(Advertisement)
admin.site.register(Shipment)
admin.site.register(Registration)

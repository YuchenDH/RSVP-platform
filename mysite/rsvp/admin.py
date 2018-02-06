from django.contrib import admin

from .models import Event, Question, Option, Vendor, Guest

admin.site.register(Event)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Vendor)
admin.site.register(Guest)

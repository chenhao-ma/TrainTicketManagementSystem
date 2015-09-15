from django.contrib import admin
from .models import UserProfile, Station, Train, ThroughStation, DirectRoute

admin.site.register(UserProfile)
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(ThroughStation)
admin.site.register(DirectRoute)


from django.contrib import admin
from .models import Hospital, Receiver, BloodSample, BloodRequest

admin.site.register(Hospital)
admin.site.register(Receiver)
admin.site.register(BloodSample)
admin.site.register(BloodRequest)

# Register your models here.

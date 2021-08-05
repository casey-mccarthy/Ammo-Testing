from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Trip)
admin.site.register(models.Vehicle)
admin.site.register(models.EmployeeType)
admin.site.register(models.Business)
admin.site.register(models.TripVehicle)
admin.site.register(models.TripEmployeeType)
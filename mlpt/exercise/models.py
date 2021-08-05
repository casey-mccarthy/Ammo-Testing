
from django.db import models
from django.db.models import Sum

# Create your models here.

class TripManager(models.Manager):

    def get_vehicle_weight(self):
        return self.get_queryset().all().aggregate(total_weight=Sum('vehicle__weight'))

    def get_vehicle_fuel(self):
        return self.get_queryset().all().aggregate(total_fuel=Sum('vehicle__fuel'))

class Vehicle(models.Model):
    """A vehicle may belong to multiple businesses and multiple trips at once."""

    name = models.CharField(max_length=50, help_text="The common name of the vehicle.")
    fuel_capacity = models.IntegerField(default=0, help_text="The total fuel capacity in gallons.")
    burn_rate = models.FloatField(default=0, help_text="The burn rate of fuel in gal/h.")
    weight = models.FloatField(default=0, help_text="The weight of the vehicle in pounds.")

    def __str__(self):
        return self.name


class Business(models.Model):
    """"""
    name = models.CharField(max_length=50, help_text="The name of the business.")

    def __str__(self):
        return self.name

class EmployeeType(models.Model):
    """Employee types can belong to many businesses."""
    name = models.CharField(max_length=50, help_text="The title/role of a type of employee.")

    def __str__(self):
        return self.name      


class Trip(models.Model):
    """A trip will be the primary object, composed of other objects that are associated with the trip."""
    name = models.CharField(max_length=128)
    vehicles = models.ManyToManyField(Vehicle, through="TripVehicle", through_fields=('trip', 'vehicle'),)
    employee_types = models.ManyToManyField(EmployeeType, through="TripEmployeeType", through_fields=('trip', 'employee_types'),)
    businesses = models.ManyToManyField(Business)
    objects = TripManager()

    class Meta:
        base_manager_name = 'objects'

    def __str__(self):
        return self.name

class TripVehicle(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class TripEmployeeType(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    employee_types = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
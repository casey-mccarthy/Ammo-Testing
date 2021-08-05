
from django.db import models
from django.db.models import Sum, F, Count
from django.db.models.query import QuerySet

# Create your models here.

class TripManager(models.Manager):

    def get_vehicle_weight(self, trip: int) -> dict:
        """Return the cumulative weight of each vehicle associated with a trip."""
        return self.get_queryset().filter(id=trip).aggregate(
            total_weight=Sum(
                F('vehicles__weight')*F('tripvehicle__quantity')
                )
            )


    def get_vehicle_quantity(self, trip: int) -> dict:
        """Returns the total number of vehicles associated with a trip."""
        return self.get_queryset().filter(id=trip).aggregate(
            total_vehicles=Sum('tripvehicle__quantity')
            )


    def get_vehicle_bingo_fuel(self, trip: int) -> dict:
        """Returns the total amount of initial fuel required to top off every vehicle on a trip."""
        return self.get_queryset().filter(id=trip).aggregate(
            total_bingo_fuel=Sum(F('vehicles__fuel_capacity') * F('tripvehicle__quantity'))
            )


    def get_vehicle_parts_count(self, trip: int):
        """Return a total count of all parts for each vehicle associated to a trip."""
        parts = Part.objects.filter(
            vehicle__in=Vehicle.objects.filter(
                trip__in=self.get_queryset().filter(id=trip)
                )
            )

        # this returns a number of perts for
        vehicles = parts.all().values('vehicle').count()
        print(vehicles)

        print(parts)
        return parts.aggregate(parts_count=Count('vehicle__parts'))

    def get_vehicle_parts_weight(self, trip: int):
        """Return a total weight of all parts for each vehicle associated to a trip."""
        parts = Part.objects.filter(
            vehicle__in=Vehicle.objects.filter(
                trip__in=self.get_queryset().filter(id=trip)
                )
            )
            
        return parts.aggregate(parts_count=Sum('vehicle__parts'))

class Part(models.Model):
    """A part to a Vehicle."""
    name = models.CharField(max_length=50, help_text="The common name of the part.")
    weight = models.IntegerField(default=0, help_text="The weight of the part.")

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    """A vehicle may belong to multiple businesses and multiple trips at once."""

    name = models.CharField(max_length=50, help_text="The common name of the vehicle.")
    fuel_capacity = models.IntegerField(default=0, help_text="The total fuel capacity in gallons.")
    burn_rate = models.FloatField(default=0, help_text="The burn rate of fuel in gal/h.")
    weight = models.FloatField(default=0, help_text="The weight of the vehicle in pounds.")
    parts = models.ManyToManyField(
        Part, 
        through="VehiclePart", 
        through_fields=('vehicle', 'part'),
        help_text="A list of vehicle parts that this vehicle contains."
        )

    def __str__(self):
        return self.name

    @property
    def parts_count(self):
        """Return the count of all parts in a vehicle."""
        return self.parts.all().aggregate(count=Sum(F('vehiclepart__quantity')))["count"]

    @property
    def parts_weight(self):
        """Return the total weight of all parts in a vehicle."""
        return self.parts.all().aggregate(weight=Sum(F('weight')))["weight"]

class Business(models.Model):
    """A business that is used to hold many persons and assets."""
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
    """Intermediate table for Trips and Vehicles assigning a quantity."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.trip}  {self.business}  {self.vehicle}  {self.quantity}"

class TripEmployeeType(models.Model):
    """Intermediate table for Trips and Employees assigning a quantity."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    employee_types = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.trip}  {self.business}  {self.employee_types}  {self.quantity}"

class VehiclePart(models.Model):
    """Intermediate table for Vehicles and Parts assigning a quantity."""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle}  {self.part}  {self.quantity}"
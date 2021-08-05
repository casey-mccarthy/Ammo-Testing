
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    trip = Trip.objects.all().first()
    weight = Trip.objects.get_vehicle_weight(trip=trip.id)
    quantities = Trip.objects.get_vehicle_quantity(trip=trip.id)
    fuel = Trip.objects.get_vehicle_bingo_fuel(trip=trip.id)
    vehicle_parts = Trip.objects.get_vehicle_parts_count(trip=trip.id)
    test = Vehicle.objects.get(id=1)

    # get all vehicles going and list their parts
    parts_list = TripVehicle.objects.filter(trip=trip.id).values('vehicle').annotate(count=Sum('vehicle__parts'))
    


    context = {
        'weight' : weight,
        'quantities' : quantities,
        'fuel' : fuel,
        'vehicle_parts' : vehicle_parts,
        'parts_list' : parts_list,
    }

    return render(request, 'exercise/home.html', context=context)
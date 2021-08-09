
from django.shortcuts import render
from .models import *


def home(request):
    """Testing view to demonstrate new structure and methods."""
    exercise = Exercise.objects.all().first()
    base_allowance = Ammo.objects.get_total_base_allowance_weight(exercise=exercise.id)
    daily_assault = Ammo.objects.get_total_daily_assault_weight(exercise=exercise.id)
    daily_sustain = Ammo.objects.get_total_daily_sustain_weight(exercise=exercise.id)
 
    context = {

        'base_allowance' : base_allowance,
        'daily_assault' : daily_assault,
        'daily_sustain' : daily_sustain,     

    }

    return render(request, 'exercise/home.html', context=context)

from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    """Testing view to demonstrate new structure and methods."""
    exercise = Exercise.objects.all().first()
    #weight = Exercise.objects.get_equipment_weight(exercise=exercise.id)
    #quantities = Exercise.objects.get_equipment_quantity(exercise=exercise.id)
    #fuel = Exercise.objects.get_equipment_bingo_fuel(exercise=exercise.id)
    #equipment_ammos = Exercise.objects.get_equipment_ammo_count(exercise=exercise.id)
    base_allowance = Ammo.objects.get_total_base_allowance_weight(exercise=exercise.id)
    #daily_assault = Ammo.objects.get_total_daily_assault_weight(exercise=exercise.id)
    #daily_sustain = Ammo.objects.get_total_daily_sustain_weight(exercise=exercise.id)
  

    # get all equipments going and list their ammos
    #ammos_list = ExerciseEquipment.objects.filter(exercise=exercise.id).values('equipment__name').annotate(count=Sum(F('equipment__ammos__weight') * F('quantity')))
    #ammos_total = ExerciseEquipment.objects.filter(exercise=exercise.id).aggregate(total_weight=Sum(F('equipment__weight') * F('quantity')))

 
    context = {
        
        'base_allowance' : base_allowance,
        #'daily_assault' : daily_assault,
        #'daily_sustain' : daily_sustain,

      
    }

    return render(request, 'exercise/home.html', context=context)
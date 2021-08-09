
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    exercise = Exercise.objects.all().first()
    #weight = Exercise.objects.get_equipment_weight(exercise=exercise.id)
    #quantities = Exercise.objects.get_equipment_quantity(exercise=exercise.id)
    #fuel = Exercise.objects.get_equipment_bingo_fuel(exercise=exercise.id)
    #equipment_ammos = Exercise.objects.get_equipment_ammo_count(exercise=exercise.id)
    ammo_weight = AmmoItem.objects.get_ammo_weight(exercise=exercise.id)
  


    # get all equipments going and list their ammos
    #ammos_list = ExerciseEquipment.objects.filter(exercise=exercise.id).values('equipment__name').annotate(count=Sum(F('equipment__ammos__weight') * F('quantity')))
    print(ammo_weight)
    #ammos_total = ExerciseEquipment.objects.filter(exercise=exercise.id).aggregate(total_weight=Sum(F('equipment__weight') * F('quantity')))

    




    

    


    context = {
        
        'ammo_weight' : ammo_weight,

      
    }

    return render(request, 'exercise/home.html', context=context)
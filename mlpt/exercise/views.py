
from django.shortcuts import render
from .models import *

# Create your views here.


def home(request):
    exercise = Exercise.objects.all().first()
    weight = Exercise.objects.get_equipment_weight(exercise=exercise.id)
    quantities = Exercise.objects.get_equipment_quantity(exercise=exercise.id)
    fuel = Exercise.objects.get_equipment_bingo_fuel(exercise=exercise.id)
    equipment_ammos = Exercise.objects.get_equipment_ammos_count(exercise=exercise.id)
    test = Equipment.objects.get(id=1)

    # get all equipments going and list their ammos
    ammos_list = ExerciseEquipment.objects.filter(exercise=exercise.id).values('equipment__name').annotate(count=Sum('equipment__ammos'))
    
    #test_list = Exercise.objects.filter(id=exercise.id).prefetch_related('equipments','equipments__ammos')
    test_list = Ammo.objects.filter(equipment__exercise=exercise.id)

    

    print(test_list)
    


    context = {
        
        'weight' : weight,
        'quantities' : quantities,
        'fuel' : fuel,
        'equipment_ammos' : equipment_ammos,
        'ammos_list' : ammos_list,
        'test_list' : test_list,
    }

    return render(request, 'exercise/home.html', context=context)
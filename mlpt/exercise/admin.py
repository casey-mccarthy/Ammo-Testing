from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Exercise)
admin.site.register(models.Equipment)
admin.site.register(models.EquipmentItem)
admin.site.register(models.Ammo)
admin.site.register(models.AmmoItem)
admin.site.register(models.Unit)
admin.site.register(models.ExerciseEdl)
admin.site.register(models.CombatLoad)
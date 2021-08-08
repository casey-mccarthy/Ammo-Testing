
from django.db import models
from django.db.models import Sum, F, Count
from django.db.models.query import QuerySet


# Create your models here.


class ExerciseManager(models.Manager):

    def get_equipment_weight(self, exercise: int) -> dict:
        """Return the cumulative weight of each equipment associated with a exercise."""
        return self.get_queryset().filter(id=exercise).aggregate(
            total_weight=Sum(
                F('equipments__weight')*F('exerciseequipment__quantity')
                )
            )


    def get_equipment_quantity(self, exercise: int) -> dict:
        """Returns the total number of equipments associated with a exercise."""
        return self.get_queryset().filter(id=exercise).aggregate(
            total_equipments=Sum('exerciseequipment__quantity')
            )


    def get_equipment_bingo_fuel(self, exercise: int) -> dict:
        """Returns the total amount of initial fuel required to top off every equipment on a exercise."""
        return self.get_queryset().filter(id=exercise).aggregate(
            total_bingo_fuel=Sum(F('equipments__fuel_capacity') * F('exerciseequipment__quantity'))
            )


    def get_equipment_ammo_count(self, exercise: int):
        """Return a total count of all ammo for each equipment associated to a exercise."""
        return Equipment.objects.filter(
                exercise__in=self.get_queryset().filter(id=exercise)
                ).aggregate(ammo_count=Count('ammos'))


    def get_equipment_ammo_weight(self, exercise: int):
        """Return a total weight of all ammo for each equipment associated to a exercise."""
        return Ammo.objects.filter(
            equipment__in=Equipment.objects.filter(
                exercise__in=self.get_queryset().filter(id=exercise)
                )
            ).aggregate(ammo_count=Sum('equipment__ammo'))


class EquipmentManager(models.Manager):

    def get_ammo_weight(self) -> dict:
        """Return the cumulative weight of each equipment associated with a exercise."""
        return self.get_queryset().filter().aggregate(
            total_weight=Sum(
                F('ammo__weight')*F('exerciseequipment__quantity')
                )
            )

# ammo
class Ammo(models.Model):
    """A part to a Equipment."""
    name = models.CharField(max_length=50, help_text="The common name of the part.")
    weight = models.IntegerField(default=0, help_text="The weight of the part.")

    def __str__(self):
        return self.name

# equipment
class Equipment(models.Model):
    """A equipment may belong to multiple unites and multiple exercises at once."""

    name = models.CharField(max_length=50, help_text="The common name of the equipment.")
    fuel_capacity = models.IntegerField(default=0, help_text="The total fuel capacity in gallons.")
    burn_rate = models.FloatField(default=0, help_text="The burn rate of fuel in gal/h.")
    weight = models.FloatField(default=0, help_text="The weight of the equipment in pounds.")
    ammos = models.ManyToManyField(
        Ammo, 
        through="EquipmentAmmo", 
        through_fields=('equipment', 'ammo'),
        help_text="A list of equipment ammo that this equipment contains."
        )

    def __str__(self):
        return self.name

    @property
    def ammo_count(self):
        """Return the count of all ammo in a equipment."""
        return self.ammo.all().aggregate(count=Sum(F('equipmentpart__quantity')))["count"]

    @property
    def ammo_weight(self):
        """Return the total weight of all ammo in a equipment."""
        return self.ammo.all().aggregate(weight=Sum(F('weight')))["weight"]

# unit
class Unit(models.Model):
    """A unit that is used to hold many persons and assets."""
    name = models.CharField(max_length=50, help_text="The name of the unit.")

    def __str__(self):
        return self.name

# troop - officer, enlisted, etc
class PeopleType(models.Model):
    """PeopleType can belong to many units."""
    name = models.CharField(max_length=50, help_text="The title/role of a type of person.")

    def __str__(self):
        return self.name      

# exercise
class Exercise(models.Model):
    """A exercise will be the primary object, composed of other objects that are associated with the exercise."""
    name = models.CharField(max_length=128)
    equipments = models.ManyToManyField(Equipment, through="ExerciseEquipment", through_fields=('exercise', 'equipment'),)
    people_types = models.ManyToManyField(PeopleType, through="ExercisePeopleType", through_fields=('exercise', 'people_type'),)
    units = models.ManyToManyField(Unit)
    objects = ExerciseManager()

    class Meta:
        base_manager_name = 'objects'

    def __str__(self):
        return self.name


class ExerciseEquipment(models.Model):
    """Intermediate table for Exercises and Equipments assigning a quantity."""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='equipment')
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.exercise}  {self.unit}  {self.equipment}  {self.quantity}"


class ExercisePeopleType(models.Model):
    """Intermediate table for Exercises and PeopleTypess assigning a quantity."""
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    people_type = models.ForeignKey(PeopleType, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    def __str__(self):
        return f"{self.exercise}  {self.unit}  {self.people_type}  {self.quantity}"


class EquipmentAmmo(models.Model):
    """Intermediate table for Equipments and Ammos assigning a quantity."""

    GROUND_COMBAT_ELEMENT = 'G'
    NON_GROUND_COMBAT_ELEMENT = 'N'

    UNIT_TYPES = [
        (GROUND_COMBAT_ELEMENT, 'Ground Combat Element'),
        (NON_GROUND_COMBAT_ELEMENT, 'Non-Ground Combat Element'),

    ]

    unit_type = models.CharField(
        max_length=1,
        choices=UNIT_TYPES,
        default=GROUND_COMBAT_ELEMENT,
    )

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    ammo = models.ForeignKey(Ammo, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.unit_type}  {self.equipment}  {self.ammo}  {self.quantity}"

    class Meta:
            constraints = [models.UniqueConstraint(fields=['equipment', 'ammo', 'unit_type'], name='EQUIPMENT_AMMO_UNIQUE')]
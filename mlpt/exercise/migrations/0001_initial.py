# Generated by Django 3.2.6 on 2021-08-06 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ammo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The common name of the part.', max_length=50)),
                ('weight', models.IntegerField(default=0, help_text='The weight of the part.')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The common name of the equipment.', max_length=50)),
                ('fuel_capacity', models.IntegerField(default=0, help_text='The total fuel capacity in gallons.')),
                ('burn_rate', models.FloatField(default=0, help_text='The burn rate of fuel in gal/h.')),
                ('weight', models.FloatField(default=0, help_text='The weight of the equipment in pounds.')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The title/role of a type of person.', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the unit.', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExercisePerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.exercise')),
                ('person_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.person')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.unit')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment', to='exercise.equipment')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.exercise')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.unit')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='equipments',
            field=models.ManyToManyField(through='exercise.ExerciseEquipment', to='exercise.Equipment'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='persons',
            field=models.ManyToManyField(through='exercise.ExercisePerson', to='exercise.Person'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='unites',
            field=models.ManyToManyField(to='exercise.Unit'),
        ),
        migrations.CreateModel(
            name='EquipmentAmmo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.equipment')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.ammo')),
            ],
        ),
        migrations.AddField(
            model_name='equipment',
            name='ammos',
            field=models.ManyToManyField(help_text='A list of equipment ammo that this equipment contains.', through='exercise.EquipmentAmmo', to='exercise.Ammo'),
        ),
    ]

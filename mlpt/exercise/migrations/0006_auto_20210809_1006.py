# Generated by Django 3.2.6 on 2021-08-09 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0005_equipmentammo_equipment_ammo_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmmoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phasing_location', models.CharField(choices=[('AE', 'Assault Element'), ('AFOE', 'Assault Follow-On Element')], default='AE', help_text='The location of the item in relation to the phasing.', max_length=4)),
                ('quantity', models.PositiveIntegerField(default=0, help_text='The quantity of an item.')),
                ('ammo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.ammo')),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentAmmoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('G', 'Ground Combat Element'), ('N', 'Non-Ground Combat Element')], default='G', max_length=1)),
                ('ammo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.ammoitem')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exercise.equipment')),
            ],
        ),
        migrations.DeleteModel(
            name='EquipmentAmmo',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='ammos',
            field=models.ManyToManyField(help_text='A list of equipment ammo that this equipment contains.', through='exercise.EquipmentAmmoItem', to='exercise.AmmoItem'),
        ),
        migrations.AddConstraint(
            model_name='equipmentammoitem',
            constraint=models.UniqueConstraint(fields=('equipment', 'ammo', 'unit_type'), name='EQUIPMENT_AMMO_UNIQUE'),
        ),
    ]

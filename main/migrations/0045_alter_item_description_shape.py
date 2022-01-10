# Generated by Django 3.2.3 on 2021-12-31 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_alter_plan_assemblies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_description',
            name='shape',
            field=models.CharField(choices=[('Round', 'Round'), ('Plate', 'Plate'), ('SQ Bar', 'SQ Bar'), ('Pipe', 'Pipe'), ('BF', 'BF'), ('Labour', 'Labour'), ('ISMC', 'ISMC'), ('ISMB', 'ISMB'), ('ISA', 'ISA'), ('Bolt', 'Bolt'), ('Nut', 'Nut'), ('RecPipe', 'RecPipe')], max_length=20),
        ),
    ]
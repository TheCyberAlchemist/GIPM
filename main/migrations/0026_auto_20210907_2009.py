# Generated by Django 3.2.3 on 2021-09-07 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_grn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grn',
            name='time_stamp',
        ),
        migrations.AddField(
            model_name='grn',
            name='grn_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='grn',
            name='value',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='item_description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.item_description'),
        ),
    ]
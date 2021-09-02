# Generated by Django 3.1 on 2021-08-30 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='item_description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='standard_weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_shape', models.TextField(blank=True, null=True)),
                ('weight_pmm', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='indent',
            name='party_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.vendor_details'),
        ),
        migrations.AlterField(
            model_name='indent',
            name='internal_diameter',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='size',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='thickness',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='width',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='indent',
            name='item_description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.item_description'),
        ),
    ]

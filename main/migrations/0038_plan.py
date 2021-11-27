# Generated by Django 3.2.3 on 2021-11-19 06:24

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0037_alter_assembly_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('item_state', main.models.JSONField(blank=True, null=True)),
                ('estimate', models.FloatField(blank=True, default=0, null=True)),
                ('assemblies', models.ManyToManyField(to='main.assembly')),
            ],
            options={
                'verbose_name_plural': 'Plan',
            },
        ),
    ]

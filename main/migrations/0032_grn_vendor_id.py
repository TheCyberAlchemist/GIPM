# Generated by Django 3.2.3 on 2021-09-15 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_merge_20210915_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='grn',
            name='vendor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.vendor_details'),
        ),
    ]

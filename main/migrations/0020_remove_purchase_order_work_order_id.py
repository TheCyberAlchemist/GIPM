# Generated by Django 3.2.3 on 2021-09-04 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20210903_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase_order',
            name='work_order_id',
        ),
    ]

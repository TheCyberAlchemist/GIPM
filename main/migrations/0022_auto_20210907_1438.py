# Generated by Django 3.2.3 on 2021-09-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_alter_work_order_wo_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_description',
            name='description',
            field=models.TextField(default='-', unique=True),
            preserve_default=False,
        ),
    ]

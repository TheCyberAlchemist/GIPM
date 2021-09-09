# Generated by Django 3.2.3 on 2021-09-07 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20210907_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grn',
            name='id',
        ),
        migrations.RemoveField(
            model_name='grn',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='grn',
            name='value',
        ),
        migrations.AddField(
            model_name='grn',
            name='order_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.order'),
            preserve_default=False,
        ),
    ]

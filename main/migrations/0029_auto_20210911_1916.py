# Generated by Django 3.2.3 on 2021-09-11 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_indent_recived_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indent',
            name='internal_diameter',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='item_description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.item_description'),
        ),
        migrations.AlterField(
            model_name='indent',
            name='size',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='thickness',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='indent',
            name='width',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='other_expanses',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='tax',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='value',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]

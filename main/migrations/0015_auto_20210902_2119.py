# Generated by Django 3.2.3 on 2021-09-02 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_rename_is_completed_purchase_order_is_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indent',
            name='work_order_id',
        ),
        migrations.RemoveField(
            model_name='work_order',
            name='PO',
        ),
        migrations.AddField(
            model_name='purchase_order',
            name='work_order_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.work_order'),
        ),
    ]
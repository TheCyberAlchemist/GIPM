# Generated by Django 3.2.3 on 2021-09-07 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20210907_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor_details',
            name='gst_no',
            field=models.TextField(blank=True, null=True),
        ),
    ]
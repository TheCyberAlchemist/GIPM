# Generated by Django 3.2.3 on 2021-09-07 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_vendor_details_gst_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_details',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
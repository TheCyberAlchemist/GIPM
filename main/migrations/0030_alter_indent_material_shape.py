# Generated by Django 3.2.3 on 2021-09-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210911_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indent',
            name='material_shape',
            field=models.TextField(default='BF'),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.2 on 2021-11-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_radiografia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiografia',
            name='codigo_estudio',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]

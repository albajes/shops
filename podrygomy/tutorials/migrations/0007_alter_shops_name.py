# Generated by Django 4.1.6 on 2023-03-03 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0006_rename_city_id_street_city_remove_shops_street_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shops',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]

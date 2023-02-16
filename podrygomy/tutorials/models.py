from django.db import models


class City(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False)


class Street(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False)
    city_id = models.ForeignKey(City, to_field='id', on_delete=models.RESTRICT)


class Address(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    house = models.CharField(max_length=10, blank=False)
    street_id = models.ForeignKey(Street, to_field='id', on_delete=models.RESTRICT)


class Shops(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=10, blank=False)
    address_id = models.ForeignKey(Address, to_field='id', on_delete=models.RESTRICT)
    open_time = models.IntegerField(blank=False)
    close_time = models.IntegerField(blank=False)

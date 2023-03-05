from django.db import models


class City(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False, unique=True, null=False)

    def __str__(self):
        return self.name


class Street(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'city'], name='StreetUniqueConstraint')
        ]

    def __str__(self):
        return self.name


class Shops(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, blank=False, null=False)
    street = models.ForeignKey(Street, on_delete=models.RESTRICT, blank=False, null=False, default='')
    house = models.CharField(max_length=10, default='')
    open_time = models.TimeField(blank=False, null=False)
    close_time = models.TimeField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['house', 'street', 'name'], name='ShopsUniqueConstraint')
        ]

    def __str__(self):
        return self.name

from rest_framework import serializers
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id',
                  'name',)


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ('id',
                  'name',
                  'city_id',)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id',
                  'house',
                  'street_id',)


class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ('id',
                  'name',
                  'address_id',
                  'open_time',
                  'close_time',)

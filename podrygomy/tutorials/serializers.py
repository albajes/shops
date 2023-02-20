from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = ('id',
#                   'house',
#                   'street_id',)


class ShopsSerializer(serializers.ModelSerializer):
    street_id = serializers.CharField(source='street_id.name')
    class Meta:
        model = Shops
        fields = ('id',
                  'name',
                  'street_id',
                  'house',
                  'open_time',
                  'close_time',)
        extra_kwargs = {'street_id': {'city': True}}

    def create(self, validated_data):
        city_data = validated_data.pop('city')
        city = City.objects.get_or_ctrate(**city_data)
        city = get_object_or_404(City, name=city_data.get('name'))
        street_data = validated_data.pop('street_id')
        print(street_data)
        street = Street.objects.get_or_create(**street_data)
        street = get_object_or_404(Street, name=street_data.get('name'))
        print(street)
        shop = Shops.objects.create(city_id=city, street_id=street, **validated_data)
        return shop
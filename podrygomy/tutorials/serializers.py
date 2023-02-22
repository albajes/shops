from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id',
                  'name',)


class StreetSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='city.name')

    class Meta:
        model = Street
        fields = ('id',
                  'name',
                  'city',)


class ShopsSerializer(serializers.ModelSerializer):
    street = serializers.CharField(source='street.name')
    city = serializers.CharField(source='city.name')

    class Meta:
        model = Shops
        fields = ('id',
                  'name',
                  'street',
                  'city',
                  'house',
                  'open_time',
                  'close_time',)
        extra_kwargs = {
            'city': {'write_only': True, 'source': 'city.name'},
        }

    def create(self, validated_data):
        print("start")
        street_data = validated_data.pop('street')
        print(street_data)
        city_data = validated_data.pop('city')
        print(city_data)

        street = Street.objects.filter(name=street_data.get("name"))
        city = City.objects.filter(name=city_data.get("name"))
        print(street)
        print(city)

        if not city:
            City.objects.get_or_create(**city_data)
            Street.objects.get_or_create(**street_data)
            city = get_object_or_404(City, name=city_data.get('city'))
            street = get_object_or_404(Street, name=street_data.get('street'))
            print(city)
            print(street)


        # if not street:
        #     print('This street is not in the database')






        # street = Street.objects.get_or_create(**street_data)
        # print(street)
        # street = get_object_or_404(Street, name=street_data.get('name'))
        # print(street)
        # shop = Shops.objects.create(street_id=street, **validated_data)
        # return shop

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

    def create(self, validated_data):
        city_data = validated_data.pop('city')
        city = City.objects.filter(name=city_data.get("name"))
        if not city:
            city = City.objects.create(**city_data)
            print(city)

        city = get_object_or_404(City, name=city_data.get('name'))
        street = Street.objects.create(**validated_data, city=city)
        return street


class ShopsSerializer(serializers.ModelSerializer):
    street = serializers.CharField(source='street.name')
    city = serializers.CharField(write_only=True, source='city.name')

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
            city = City.objects.create(**city_data)
            print(city)
            street = Street.objects.get_or_create(**street_data, city=city)
            print(street)

        if not street:
            city = get_object_or_404(City, name=city_data.get('name'))
            street = Street.objects.create(**street_data, city=city)
            print(street)

        city = get_object_or_404(City, name=city_data.get('name'))
        street = get_object_or_404(Street, name=street_data.get('name'), city=city.id)
        shop = Shops.objects.create(**validated_data, street=street)
        return shop

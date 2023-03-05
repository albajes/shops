from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import *
import logging

_logger = logging.getLogger(__name__)


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
        _logger.debug("Start creating Street object")
        city_data = validated_data.pop('city')
        _logger.debug("City data: %s", city_data)
        city = City.objects.filter(name=city_data.get("name"))
        if not city:
            _logger.debug("City by name %s not found in data base. Start creating", city_data.get("name"))
            City.objects.create(**city_data)

        city = get_object_or_404(City, name=city_data.get('name'))
        _logger.debug("Object data City from table: %s", city)
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
        _logger.debug('Start creating Shop object')
        street_data = validated_data.pop('street')
        _logger.debug('Street data: %s', street_data)
        city_data = validated_data.pop('city')
        _logger.debug('City data: %s', city_data)
        street = Street.objects.filter(name=street_data.get('name'))
        city = City.objects.filter(name=city_data.get('name'))

        if not city:
            _logger.debug('City by name %s not found in data base. Start creating', city_data.get("name"))
            City.objects.create(**city_data)

        city = get_object_or_404(City, name=city_data.get('name'))

        if not street:
            street = Street.objects.create(**street_data, city=city)
            print(street)

        street = get_object_or_404(Street, name=street_data.get('name'), city=city.id)
        shop = Shops.objects.create(**validated_data, street=street)
        return shop

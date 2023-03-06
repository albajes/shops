from django.db import IntegrityError
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response

from .serializers import *
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
import datetime
import logging


_logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
def cities(request):
    _logger.debug('Rest request %s /api/city received', request.method)
    if request.method == 'GET':
        all_cities = City.objects.all()
        if not all_cities:
            _logger.warning('No cities were found in the database. 404 response is returned')
            return Response('Cities not created', status=status.HTTP_404_NOT_FOUND)

        _logger.debug('Found %s cities', len(all_cities))
        all_cities_serializer = CitySerializer(all_cities, many=True)
        return JsonResponse(all_cities_serializer.data, safe=False)

    elif request.method == 'POST':
        all_cities_serializer = CitySerializer(data=request.data)
        if all_cities_serializer.is_valid():
            _logger.debug('The received data is valid. The city start saving')
            all_cities_serializer.save()
            return Response(all_cities_serializer.data, status=status.HTTP_201_CREATED)
        _logger.warning('The received data is no valid. 400 response is returned')
        return Response(all_cities_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def streets_by_city_id(request):
    _logger.debug('Rest request %s /api/street received', request.method)
    if request.method == 'GET':
        var_city_id = request.query_params.get('city_id')
        _logger.debug('Parameter city_id %s received', var_city_id)
        if var_city_id is None or not var_city_id.isdigit():
            _logger.warning('Parameter city_id %s not number. 400 response is returned', var_city_id)
            return Response('City expected', status=status.HTTP_400_BAD_REQUEST)
        streets = Street.objects.filter(city_id=var_city_id)
        streets_serializer = StreetSerializer(streets, many=True)
        return JsonResponse(streets_serializer.data, safe=False)

    elif request.method == 'POST':
        street_serializer = StreetSerializer(data=request.data)
        if street_serializer.is_valid():
            _logger.debug("The received data is valid. The street start saving")
            try:
                street_serializer.save()
            except IntegrityError:
                return Response('Such data already exists', status=status.HTTP_400_BAD_REQUEST)
            return Response(street_serializer.data, status=status.HTTP_201_CREATED)
        _logger.warning("The received data is not valid. 400 response is returned")
        return Response(street_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def create_shop(request):
    _logger.debug("Rest request %s /api/shop received", request.method)
    if request.method == 'POST':
        shop_serializer = ShopsSerializer(data=request.data)
        if shop_serializer.is_valid():
            _logger.debug("The received data is valid. The shop start saving")
            try:
                shop = shop_serializer.save()
            except IntegrityError:
                return Response('Such data already exists', status=status.HTTP_400_BAD_REQUEST)
            slovar = dict.fromkeys({'id'}, shop.id)
            return Response(slovar, status=status.HTTP_201_CREATED)
        _logger.warning("The received data is not valid. 400 response is returned")
        return Response(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        _logger.info("Get shop request with parameters:")
        var_street_id = request.query_params.get('street')
        var_city_id = request.query_params.get('city')
        var_open = request.query_params.get('open')
        all_shops = Shops.objects.all()
        if var_city_id is not None and var_city_id.isdigit():
            _logger.info("Set city_id: %s", var_city_id)
            streets = Street.objects.filter(city_id=var_city_id)
            streets_id_list = [streets.id for streets in streets]
            all_shops = all_shops.filter(street_id__in=streets_id_list)

        if var_street_id is not None and var_street_id.isdigit():
            _logger.info("Set street_id: %s", var_street_id)
            all_shops = all_shops.filter(street_id=var_street_id)

        if var_open is not None and var_open.isdigit():
            _logger.info("Set open: %s", var_open)
            now = datetime.datetime.now().time()
            _logger.info("Time now: %s h", now)

            if var_open == '0':
                all_shops = all_shops.filter(Q(open_time__gt=now) | Q(close_time__lte=now))
            elif var_open == '1':
                all_shops = all_shops.filter(open_time__lte=now, close_time__gt=now)

        shops_s = ShopsSerializer(all_shops, many=True)
        return JsonResponse(shops_s.data, safe=False)

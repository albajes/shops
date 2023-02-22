from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import *
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from django.http.response import JsonResponse
import datetime


@api_view(['GET', 'POST'])
def cities(request):
    if request.method == 'GET':
        all_cities = City.objects.all()
        if not all_cities:
            return Response('Cities not created', status=status.HTTP_404_NOT_FOUND)

        all_cities_serializer = CitySerializer(all_cities, many=True)
        return JsonResponse(all_cities_serializer.data, safe=False)

    elif request.method == 'POST':
        all_cities_serializer = CitySerializer(data=request.data)
        if all_cities_serializer.is_valid():
            all_cities_serializer.save()
            return Response(all_cities_serializer.data, status=status.HTTP_201_CREATED)
        return Response(all_cities_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def streets_by_city_id(request):
    if request.method == 'GET':
        var_city_id = request.query_params.get('city_id')
        if var_city_id is None or not var_city_id.isdigit():
            return Response('City id expected', status=status.HTTP_400_BAD_REQUEST)
        streets = Street.objects.filter(city_id=var_city_id)
        streets_serializer = StreetSerializer(streets, many=True)
        return JsonResponse(streets_serializer.data, safe=False)

    elif request.method == 'POST':
        street_serializer = StreetSerializer(data=request.data)
        if street_serializer.is_valid():
            street_serializer.save()
            return Response(street_serializer.data, status=status.HTTP_201_CREATED)
        return Response(street_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def create_shop(request):
    try:
        shop = Shops.objects.all()
    except Shops.DoesNotExist:
        return Response(shop.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        shop_serializer = ShopsSerializer(data=request.data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return Response(shop_serializer.data, status=status.HTTP_201_CREATED)
        return Response(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        shop.delete()
        return Response(status=204)

    elif request.method == 'GET':
        var_street_id = request.query_params.get('street')
        var_city_id = request.query_params.get('city')
        var_open = request.query_params.get('open')
        all_shops = Shops.objects.all()
        if var_city_id is not None and var_city_id.isdigit():
            streets = Street.objects.filter(city_id=var_city_id)
            streets_id_list = [streets.id for streets in streets]
            all_shops = all_shops.filter(street_id__in=streets_id_list)

        if var_street_id is not None and var_street_id.isdigit():
            all_shops = all_shops.filter(street_id=var_street_id)

        if var_open is not None and var_open.isdigit():
            now = datetime.datetime.now().hour
            print('vremya')
            print(now)
            print('varopen')
            print(var_open)
            if var_open == 0:
                all_shops = all_shops.filter(Q(open_time__qt=now) or Q(close_time__lt=now))
            elif var_open == 1:
                all_shops = all_shops.filter(Q(open_time__lt=now) and Q(close_time__qt=now))


        shops_s = ShopsSerializer(all_shops, many=True)
        return JsonResponse(shops_s.data, safe=False)

        # if var_street_id is not None and var_street_id.isdigit():
        #     street

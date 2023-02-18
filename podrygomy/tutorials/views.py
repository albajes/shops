from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from .serializers import *
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from django.http.response import JsonResponse


@api_view(['GET'])
def cities(request):
    if request.method == 'GET':
        var_cities = City.objects.all()

        var_cities_serializer = CitySerializer(var_cities, many=True)
        return JsonResponse(var_cities_serializer.data, safe=False)


@api_view(['GET'])
def streets_by_city_id(request):
    if request.method == 'GET':
        var_city_id = request.query_params.get('city_id')
        if var_city_id is None or not var_city_id.isdigit():
            return Response('What are you doing?', status=status.HTTP_400_BAD_REQUEST)
        streets = Street.object.filter(city_id=var_city_id)
        streets_serializer = StreetSerializer(streets, many=True)
        return JsonResponse(streets_serializer.data, safe=False)
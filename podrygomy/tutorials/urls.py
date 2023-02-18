from django.urls import path
from .views import *

urlpatterns = [
    path('/city', cities),
    path('api/city/street', streets_by_city_id),
    path('api/shop', create_shop)
]
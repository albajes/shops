from django.urls import path
from podrygomy.tutorials import views

urlpatterns = [
    path('api/city', views.cities),
    path('api/city/street', views.streets_by_city_id),
    path('api/shop', views.create_shop)
]
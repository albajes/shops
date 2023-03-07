from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('city', CityViewSet, basename='city')
router.register('street', StreetViewSet, basename='street')
router.register('shop', ShopViewSet, basename='shop')
urlpatterns = router.urls

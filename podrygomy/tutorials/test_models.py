from django.test import TestCase

from .models import *


class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='TEST_CITY')

    def test_name_max_length(self):
        city = City.objects.get(name='TEST_CITY')
        max_length = city._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_have_city(self):
        city = City.objects.get(name='TEST_CITY')
        all_cities = City.objects.all()
        self.assertTrue(city in all_cities)


class StreetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        city = City.objects.create(name='TEST_CITY')
        Street.objects.create(name='TEST_STREET', city=city)

    def test_name_max_length(self):
        street = Street.objects.get(name='TEST_STREET')
        max_length = street._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_have_street(self):
        street = Street.objects.get(name='TEST_STREET')
        all_streets = Street.objects.all()
        self.assertTrue(street in all_streets)


class ShopsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        city = City.objects.create(name='TEST_CITY')
        street = Street.objects.create(name='TEST_STREET', city=city)
        Shops.objects.create(name='TEST_SHOP', street=street, house=1, open_time='7:00:00', close_time='19:00:00')

    def test_name_max_length(self):
        shop = Shops.objects.get(name='TEST_SHOP')
        max_length_shop = shop._meta.get_field('name').max_length
        max_length_house = shop._meta.get_field('house').max_length
        self.assertEqual(max_length_shop, 30)
        self.assertEqual(max_length_house, 10)

    def test_have_shop(self):
        shop = Shops.objects.get(name='TEST_SHOP')
        all_shops = Shops.objects.all()
        self.assertTrue(shop in all_shops)

from django.test import TestCase
from freezegun import freeze_time
from .views import *
from datetime import datetime


class CityViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        City.objects.create(name='TEST_CITY')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/city')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_new_city(self):
        response = self.client.post('/api/city', {'name': 'NEW_TEST_CITY'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/city')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class StreetViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        city = City.objects.create(name='TEST_CITY')
        Street.objects.create(name='TEST_STREET', city=city)

    def test_view_url_expect_error(self):
        response = self.client.get('/api/street')
        self.assertEqual(response.status_code, 400)

    def test_view_url_get_street_by_city(self):
        city = City.objects.get(name='TEST_CITY')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_view_url_get_street_by_not_exist_city(self):
        response = self.client.get('/api/street?city_id=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_create_new_street_with_exist_city(self):
        response = self.client.post('/api/street', {'name': 'NEW_TEST_STREET', 'city': 'TEST_CITY'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='TEST_CITY')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        city = City.objects.all()
        self.assertEqual(len(city), 1)

    def test_create_new_street_with_not_exist_city(self):
        response = self.client.post('/api/street', {'name': 'not_exist_street', 'city': 'not_exist_city'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='not_exist_city')
        response = self.client.get('/api/street?city_id=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        city = City.objects.all()
        self.assertEqual(len(city), 2)


class ShopsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        city = City.objects.create(name='TEST_CITY_1')
        street = Street.objects.create(name='TEST_STREET_1', city=city)
        Street.objects.create(name='TEST_STREET_2', city=city)
        Shops.objects.create(name='TEST_SHOP_1', street=street, house=1, open_time='7:00:00', close_time='15:00:00')
        Shops.objects.create(name='TEST_SHOP_2', street=street, house=2, open_time='7:00:00', close_time='19:00:00')
        street = Street.objects.get(name='TEST_STREET_2')
        Shops.objects.create(name='TEST_SHOP_3', street=street, house=3, open_time='7:00:00', close_time='23:00:00')
        city = City.objects.create(name='TEST_CITY_2')
        street = Street.objects.create(name='TEST_STREET_3', city=city)
        Street.objects.create(name='TEST_STREET_4', city=city)
        Shops.objects.create(name='TEST_SHOP_4', street=street, house=4, open_time='9:00:00', close_time='23:00:00')
        Shops.objects.create(name='TEST_SHOP_5', street=street, house=5, open_time='10:00:00', close_time='19:00:00')
        street = Street.objects.get(name='TEST_STREET_4')
        Shops.objects.create(name='TEST_SHOP_6', street=street, house=6, open_time='12:00:00', close_time='21:00:00')

    def test_view_url_expect_error(self):
        response = self.client.get('/api/shop')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    def test_view_url_get_shops_by_city_id(self):
        city = City.objects.get(name='TEST_CITY_1')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_view_url_get_shops_by_street_id(self):
        street = Street.objects.get(name='TEST_STREET_1')
        response = self.client.get('/api/shop?street=' + str(street.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    @freeze_time("09:00:00")
    def test_view_url_get_shops_by_open_1_with_now_9_h(self):
        datetime.now()
        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    @freeze_time("08:00:00")
    def test_view_url_get_shops_by_open_1_with_now_8_h(self):
        datetime.now()
        response = self.client.get('/api/shop?open=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    @freeze_time("20:00:00")
    def test_view_url_get_shops_by_closed_0_with_now_20_h(self):
        datetime.now()
        response = self.client.get('/api/shop?open=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    @freeze_time("23:20:00")
    def test_view_url_get_shops_by_closed_0_with_now_20_h(self):
        datetime.now()
        response = self.client.get('/api/shop?open=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)

    @freeze_time("20:00:00")
    def test_view_url_get_shops_by_open_1_and_city_id_with_now_20_h(self):
        datetime.now()
        city = City.objects.get(name='TEST_CITY_1')
        response = self.client.get('/api/shop?open=1&city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    @freeze_time("11:00:00")
    def test_view_url_get_shops_by_closed_0_and_city_id_with_now_11_h(self):
        datetime.now()
        city = City.objects.get(name='TEST_CITY_2')
        response = self.client.get('/api/shop?open=0&city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_new_shop_with_exist_city_and_Street(self):
        response = self.client.post('/api/shop', {'name': 'Best_Shop', 'street': 'TEST_STREET_1', 'city': 'TEST_CITY_1',
                                                  'house': '1', 'open_time': '8:00:00', 'close_time': '22:00:00'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='TEST_CITY_1')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        city = City.objects.all()
        self.assertEqual(len(city), 2)
        street = Street.objects.all()
        self.assertEqual(len(street), 4)

    def test_create_new_shop_with_exist_city_and_not_exist_Street(self):
        response = self.client.post('/api/shop', {'name': 'New_Shop', 'street': 'New_Street', 'city': 'TEST_CITY_2',
                                                  'house': '5', 'open_time': '8:00:00', 'close_time': '22:00:00'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='TEST_CITY_2')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
        city = City.objects.all()
        self.assertEqual(len(city), 2)
        street = Street.objects.all()
        self.assertEqual(len(street), 5)

    def test_create_new_shop_with_not_exist_city_and_Street(self):
        response = self.client.post('/api/shop', {'name': 'New_Shop', 'street': 'NewnewStreet', 'city': 'NewnewCity',
                                                  'house': '5', 'open_time': '8:00:00', 'close_time': '22:00:00'})
        self.assertEqual(response.status_code, 201)
        city = City.objects.get(name='NewnewCity')
        response = self.client.get('/api/shop?city=' + str(city.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        city = City.objects.all()
        self.assertEqual(len(city), 3)
        street = Street.objects.all()
        self.assertEqual(len(street), 5)
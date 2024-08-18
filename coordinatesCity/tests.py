from rest_framework.test import APITestCase
from rest_framework import status
from coordinatesCity.models import city
from django.contrib.auth.models import User

class CityAPITests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin')
        self.client.login(username='admin', password='admin')
        self.valid_city_data = {'cityName': 'Москва'}
        self.invalid_city_data = {'cityName': ''}

    def test_add_city_success(self):
        response = self.client.post('/api/coordinatesCity/createCity/', self.valid_city_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(city.City.objects.count(), 1)
        self.assertEqual(city.City.objects.get().cityName, 'Москва')
    
    def test_add_existing_city(self):
        self.client.post('/api/coordinatesCity/createCity/', self.valid_city_data, format='json')
        response = self.client.post('/api/coordinatesCity/createCity/', self.valid_city_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_city_success(self):
        self.client.post('/api/coordinatesCity/createCity/', self.valid_city_data, format='json')
        response = self.client.delete('/api/coordinatesCity/deleteCity/Москва/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(city.City.objects.count(), 0)
    
    def test_delete_non_existent_city(self):
        response = self.client.delete('/api/coordinatesCity/deleteCity/Москва/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_city_info_success(self):
        self.client.post('/api/coordinatesCity/createCity/', self.valid_city_data, format='json')
        response = self.client.get('/api/coordinatesCity/getCity/Москва/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cityName'], 'Москва')
    
    def test_get_city_info_not_found(self):
        response = self.client.get('/api/coordinatesCity/getCity/NonexistentCity/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_find_nearest_cities_success(self):
        # Добавьте несколько городов с координатами
        self.client.post('/api/coordinatesCity/createCity/', {'cityName': 'Москва'}, format='json')
        self.client.post('/api/coordinatesCity/createCity/', {'cityName': 'Saint Petersburg'}, format='json')
        response = self.client.post('/api/coordinatesCity/nearCity/', {'latitude': 55.0, 'longitude': 37.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Убедитесь, что вернуто 2 города

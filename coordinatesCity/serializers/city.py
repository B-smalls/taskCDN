from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ParseError, ValidationError
from coordinatesCity.models.city import City
from coordinatesCity.utils.ExternalApi import getCoordinates
#from coordinatesCity.


#Сериализатор для создания записи
class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'cityName', 
            'latitude', 
            'longitude'
            )
        read_only_fields = ('latitude', 'longitude')

    def create(self, validated_data):
        city_name = validated_data.get('cityName')

        # Проверка - существует ли город с таким именем
        if City.objects.filter(cityName=city_name).exists():
            raise ValidationError(f"City with the name '{city_name}' already exists.")
        
        try:
            with transaction.atomic():
                # Получаем координаты города
                latitude, longitude = getCoordinates.get_coordinates(city_name)

                if latitude is None or longitude is None:
                    raise ValueError("Coordinates could not be determined for the provided city name.")
                
                # Создаем запись в базе данных
                city = City.objects.create(
                    cityName=city_name,
                    latitude=latitude,
                    longitude=longitude
                )

        except Exception as e:
            raise ParseError(f"Error created: {e}")

        return city
    
# Сериализатор для удаления записи
class CityDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['cityName']  # Поле для удаления

    def validate_cityName(self, value):
        if not City.objects.filter(cityName=value).exists():
            raise serializers.ValidationError("City with this name does not exist.")
        return value

# Сериализатор просмотра всех городов
class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'cityName', 'latitude', 'longitude']

# Сериализатор просмотра отдельного города
class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'cityName', 'latitude', 'longitude']

# Сериализатор для нахождения двух ближайших городов
class NearestCitiesSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def validate(self, data):
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            raise serializers.ValidationError("Both latitude and longitude are required.")
        return data

    def get_nearest_cities(self):
        latitude = self.validated_data.get('latitude')
        longitude = self.validated_data.get('longitude')

        # Находим два ближайших города по расстоянию от заданных координат
        cities = City.objects.all()
        nearest_cities = sorted(cities, key=lambda city: ((city.latitude - latitude) ** 2 + (city.longitude - longitude) ** 2) ** 0.5)[:2]

        return [city.cityName for city in nearest_cities]

    def to_representation(self, instance):
        nearest_cities = self.get_nearest_cities()
        return {
            'nearest_city_1': nearest_cities[0],
            'nearest_city_2': nearest_cities[1]
        }
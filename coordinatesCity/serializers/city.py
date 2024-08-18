from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ParseError

from coordinatesCity.models.city import City
from utils.ExternalApi import getCoordinates
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
class CityDeleteSerializer(serializers.Serializer):
    cityName = serializers.CharField(max_length=100)

    def validate_cityName(self, value):
        # Проверяем, что город с таким названием существует
        if not City.objects.filter(cityName=value).exists():
            raise serializers.ValidationError("City with this name does not exist.")
        return value

    def delete(self):
        city_name = self.validated_data['cityName']
        city = City.objects.get(cityName=city_name)
        city.delete()
        return {"message": f"City '{city_name}' has been deleted."}
    

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

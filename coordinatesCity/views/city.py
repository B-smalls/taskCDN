from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from coordinatesCity.models.city import City
from coordinatesCity.serializers import city
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import generics

from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    post=extend_schema(request=city.CityCreateSerializer,
                      summary='Добавление города', tags=['Города']),
)
# Представление для создания записи
class CityCreateView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = city.CityCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Failed to create city."}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    delete=extend_schema(request=city.CityDeleteSerializer,
                      summary='Удаление города', tags=['Города']),
)
class CityDeleteView(generics.DestroyAPIView):
    serializer_class = city.CityDeleteSerializer
    queryset = City.objects.all()
    lookup_field = 'cityName'  # Поле, по которому будет осуществляться удаление

    def get_object(self):
        # Переопределяем метод для поиска объекта по `cityName` вместо `id`
        city_name = self.kwargs.get(self.lookup_field)
        return City.objects.get(cityName=city_name)
    

@extend_schema_view(
    get=extend_schema(request=city.CityListSerializer,
                      summary='Получение всех городов', tags=['Города']),
)
# Представление для вывода всех городов
class CityListView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = city.CityListSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": "Failed to retrieve city list."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(request=city.CityDetailSerializer,
                      summary='Получение информации одного города', tags=['Города']),
)
# Представление для вывода информации о конкретном городе
class CityDetailView(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = city.CityDetailSerializer
    lookup_field = 'cityName'

    def get_object(self):
        city_name = self.kwargs.get('cityName')
        try:
            return City.objects.get(cityName=city_name)
        except City.DoesNotExist:
            raise NotFound(f"City with name '{city_name}' not found.")

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to retrieve city."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(request=city.NearestCitiesSerializer,
                      summary='Нахождение двух ближайших городов', tags=['Города']),
)
# Представление для нахождения двух ближайших городов
class NearestCitiesView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            serializer = city.NearestCitiesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            nearest_cities = serializer.get_nearest_cities()
            return Response(serializer.to_representation(nearest_cities), status=status.HTTP_200_OK)
        except ParseError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Failed to find nearest cities."}, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path
from coordinatesCity.views import city  

urlpatterns = [
    path('coordinatesCity/createCity/', city.CityCreateView.as_view(), name="createCity"),
    path('coordinatesCity/deleteCity/<str:cityName>/', city.CityDeleteView.as_view(), name="deleteCity"),
    path('coordinatesCity/getCity/<str:cityName>/', city.CityDetailView.as_view(), name="getCity"),
    path('coordinatesCity/getAllCity/', city.CityListView.as_view(), name="getAllCity"),
    path('coordinatesCity/nearCity/', city.NearestCitiesView.as_view(), name="nearCity"),
]
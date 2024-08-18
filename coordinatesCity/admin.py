from django.contrib import admin

from coordinatesCity.models.city import City
# Register your models here.

@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ('id', 'cityName', 'latitude', 'longitude')
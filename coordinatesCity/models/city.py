from django.db import models

# Модель City
class City(models.Model):
    cityName = models.CharField("cityName", max_length=100)
    latitude = models.FloatField("latitude")
    longitude = models.FloatField("longitude")

import requests
from config import settings

# Функция для получения координат
def get_coordinates(city_name):
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        'q': city_name,
        'key': settings.API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get('hits'):
            latitude = data['hits'][0]['point']['lat']
            longitude = data['hits'][0]['point']['lng']
            return latitude, longitude
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching coordinates: {e}")
    
    return None, None



from django.urls import path
from .views import gee_mapserver

map_api_url_patterns = [
    path('tiles/gee/<int:z>/<int:x>/<int:y>', gee_mapserver, name="gee_mapserver"),
]


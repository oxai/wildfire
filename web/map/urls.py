from django.urls import path
from .views import gee_mapserver, fpa_fod_fire_location, modis_fire_location

map_api_url_patterns = [
    path('tiles/<platform>/<sensor>/<product>/<method>/<int:z>/<int:x>/<int:y>/<from_date>/<until_date>',
         gee_mapserver, name="gee_mapserver"),
    path('fpa_fod/<from_date>/<until_date>/<int:min_fire_size>',
         fpa_fod_fire_location, name="fpa_fod_fire_location"),
    path('modis_fire/<from_date>/<until_date>/<int:confidence>',
         modis_fire_location, name="modis_fire_location"),
]


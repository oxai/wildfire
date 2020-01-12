from django.shortcuts import render, HttpResponse
import urllib.request
from resources.gee.methods import get_image_collection_asset
from web import config


# Create your views here.
def home(request):
    return render(request, 'home.html', {'mapkey': config.MAP_KEY})


# Create your views here.
def gee_mapserver(request, z, x, y):

    url = get_image_collection_asset(
        platform="landsat",
        sensor="8",
        product="surface",
        date_from="2019-12-01",
        date_to="2019-12-30",
        reducer='median'
    )

    with urllib.request.urlopen(url.format(z=z, x=x, y=y)) as response:
        tile = response.read()

    return HttpResponse(tile, content_type="image/jpeg")

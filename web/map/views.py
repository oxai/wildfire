from django.shortcuts import render, HttpResponse
import urllib.request
from resources.gee.methods import get_ee_product
from resources.gee.tile_loader import GeeTileLoader, TileQuery
from web import config
from PIL import Image


# Create your views here.
def home(request):
    return render(request, 'home.html', {'mapkey': config.MAP_KEY})


# Create your views here.
def gee_mapserver(request, z, x, y):

    loader = GeeTileLoader()

    ee_product = get_ee_product(
        platform="landsat",
        sensor="8",
        product="raw"
    )

    query = TileQuery(x=x, y=y, z=z, date_from="2019-12-01", date_to="2019-12-30", reducer="median")

    out = loader.visualise(ee_product, query)
    out = (out * 255).astype('uint8')

    out = Image.fromarray(out, 'RGB')

    response = HttpResponse(content_type='image/jpg')
    out.save(response, "JPEG")
    return response

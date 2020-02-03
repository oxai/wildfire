from django.shortcuts import render, HttpResponse
from resources.gee.methods import get_ee_product
from resources.gee.tile_loader import GeeProductTileLoader, TileDateRangeQuery


# Create your views here.
def home(request):
    # return render(request, 'home.html')
    return HttpResponse("API Endpoint")


# Create your views here.
def gee_mapserver(request, platform, sensor, product, method, z, x, y):

    loader = GeeProductTileLoader()

    ee_product = get_ee_product(
        platform=platform,
        sensor=sensor,
        product=product
    )

    query = TileDateRangeQuery(x=x, y=y, z=z, date_from="2019-12-01", date_to="2019-12-30", reducer="median")

    out = loader.visualise(ee_product, query, method=method, subdir="map")

    response = HttpResponse(content_type='image/png')
    out.save(response, "PNG")
    return response

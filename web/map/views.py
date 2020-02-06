from django.shortcuts import render, HttpResponse
from resources.gee.methods import get_ee_product
from resources.gee.tile_loader import GeeProductTileLoader, TileDateRangeQuery
from resources.gee.vis_handler import visualise_image_from_ee_product


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

    out = loader.load(ee_product, query, subdir="map")
    image = visualise_image_from_ee_product(out, ee_product, method=method)

    response = HttpResponse(content_type='image/png')
    image.save(response, "PNG")
    return response

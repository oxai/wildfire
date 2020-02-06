import ee
from .products import EE_PRODUCTS
from . import cloud_mask as cm
from ..utils.gis import get_bbox_corners_for_tile, get_tile_pixel_scale_from_zoom
from datetime import datetime
from collections import namedtuple


TileDateRangeQuery = namedtuple("Query", "x y z date_from date_to reducer")
TileDateQuery = namedtuple("Query", "x y z date")


def image_to_map_id(ee_image, vis_params=None):
    """
    Get map_id parameters
    """
    if vis_params is None:
        vis_params = {}
    map_id = ee_image.getMapId(vis_params)
    map_id_params = {
        'mapid': map_id['mapid'],
        'token': map_id['token']
    }
    return map_id_params


def get_ee_product(platform, sensor, product):
    return EE_PRODUCTS[platform][sensor][product]


def get_ee_product_name(ee_product):
    return ee_product['collection'].replace('/', '-')


def get_ee_collection_from_product(ee_product, q: TileDateRangeQuery):
    """
    Get tile url for image collection asset.
    """
    if not q.date_from or not q.date_to:
        raise Exception("Too many images to handle. Define data_from and date_to")

    collection = ee_product['collection']
    cloud_mask = ee_product.get('cloud_mask', None)

    geometry = ee.Geometry.Rectangle(get_bbox_corners_for_tile(q.x, q.y, q.z))

    ee_collection = ee.ImageCollection(collection)\
        .filter(
            ee.Filter.date(q.date_from, q.date_to)
        )\
        .filterBounds(geometry)

    if cloud_mask:
        cloud_mask_func = getattr(cm, cloud_mask, None)
        if cloud_mask_func:
            ee_collection = ee_collection.map(cloud_mask_func)

    return ee_collection


def get_ee_image_from_product(ee_product, q: TileDateRangeQuery):
    ee_collection = get_ee_collection_from_product(ee_product, q)
    ee_image = getattr(ee_collection, q.reducer)()
    return ee_image


def get_ee_image_list_from_collection(ee_collection):
    ee_images = ee_collection.toList(ee_collection.size())
    return [ee.Image(ee_images.get(i)) for i in range(ee_collection.size().getInfo())]


def get_ee_image_date(ee_image):
    timestamp = ee_image.get("system:time_start").getInfo()
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")


def get_map_tile_url(ee_image, vis_params=None):
    tile_url_template = "https://earthengine.googleapis.com/v1alpha/{mapid}/tiles/{{z}}/{{x}}/{{y}}"
    map_id_params = image_to_map_id(ee_image, vis_params)
    return tile_url_template.format(**map_id_params)


def get_image_download_url(ee_image, bbox, scale, name=None):
    name = {'name': name} if name else {}
    geometry = ee.Geometry.Rectangle(bbox)

    return ee_image.getDownloadURL({
        **name,
        "scale": scale,
        'crs': 'EPSG:3857',     # WGS 84 Web Mercator
        "region": geometry["coordinates"]
    })


def get_image_download_url_for_tile(ee_image, x_tile, y_tile, zoom, tile_size, name=None):
    bbox = get_bbox_corners_for_tile(x_tile, y_tile, zoom)
    scale = get_tile_pixel_scale_from_zoom(zoom, tile_size)
    print(f"Downloading image tile of size {tile_size}x{tile_size} pixels with {scale:.2f} m resolution")
    return get_image_download_url(ee_image, bbox, scale, name)


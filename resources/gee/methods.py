import ee
from .products import EE_PRODUCTS
from . import cloud_mask as cm


def image_to_map_id(image_name, vis_params=None):
    """
    Get map_id parameters
    """
    if vis_params is None:
        vis_params = {}
    ee_image = ee.Image(image_name)
    map_id = ee_image.getMapId(vis_params)
    map_id_params = {
        'mapid': map_id['mapid'],
        'token': map_id['token']
    }
    return map_id_params


def get_image_collection_asset(platform, sensor, product, date_from=None, date_to=None, reducer='median'):
    """
    Get tile url for image collection asset.
    """
    if not date_from or not date_to:
        raise Exception("Too many images to handle. Define data_from and date_to")

    ee_product = EE_PRODUCTS[platform][sensor][product]

    collection = ee_product['collection']
    index = ee_product.get('index', None)
    vis_params = ee_product.get('vis_params', None)
    cloud_mask = ee_product.get('cloud_mask', None)

    print(f'Image Collection Name: {collection}')
    print(f'Band Selector: {index}')
    print(f'Vis Params: {vis_params}')

    tile_url_template = "https://earthengine.googleapis.com/v1alpha/{mapid}/tiles/{{z}}/{{x}}/{{y}}"

    ee_collection = ee.ImageCollection(collection)

    ee_filter_date = ee.Filter.date(date_from, date_to)
    ee_collection = ee_collection.filter(ee_filter_date)

    if index:
        ee_collection = ee_collection.select(index)

    if cloud_mask:
        cloud_mask_func = getattr(cm, cloud_mask, None)
        if cloud_mask_func:
            ee_collection = ee_collection.map(cloud_mask_func)

    ee_collection = getattr(ee_collection, reducer)()

    map_id_params = image_to_map_id(ee_collection, None)

    return tile_url_template.format(**map_id_params)

import ee


def add_mask(image, mask):
    return image.addBands(mask).copyProperties(image, ["system:time_start"])


def mask_l8_sr(image):
    """
    Derived From: https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C01_T1_SR
    """
    # Bits 3 and 5 are cloud shadow and cloud, respectively.
    cloudShadowBitMask = (1 << 3)
    cloudsBitMask = (1 << 5)

    # Get the pixel QA band.
    qa = image.select(['pixel_qa'], ['cloud_mask'])

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return add_mask(image, mask)


def mask_l8_raw(image):
    # Bits 3 and 5 are cloud shadow and cloud, respectively.
    cloudShadowBitMask = (1 << 4)

    # Get the pixel QA band.
    qa = image.select(['BQA'], ['cloud_mask'])

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
    return add_mask(image, mask)


def cloud_mask_l457(image):
    """
    Derived From: https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_SR
    """
    qa = image.select(['pixel_qa'], ['cloud_mask'])

    # If the cloud bit (5) is set and the cloud confidence (7) is high
    # or the cloud shadow bit is set (3), then it's a bad pixel.
    cloud = qa.bitwiseAnd(1 << 5).And(qa.bitwiseAnd(1 << 7)).Or(qa.bitwiseAnd(1 << 3))

    # Remove edge pixels that don't occur in all bands
    occur_all = image.mask().reduce(ee.Reducer.min())
    mask = cloud.Not().And(occur_all)

    return add_mask(image, mask)


def mask_s2_clouds(image):
    """
    Derived from: https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2
    """
    qa = image.select(['QA60'], ['cloud_mask'])

    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))

    return image.divide(10000).addBands(mask).copyProperties(image, ["system:time_start"])

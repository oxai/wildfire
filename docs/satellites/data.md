## Satellite Image Providers

There are many sources that host publicly available satellite images.
We list a few alternatives below:

- [Google Earth Engine](https://earthengine.google.com/)
    Hosts a wide collection of publicly available satellite imagery data, 
    including but not limited to Sentinel, Landsat, MODIS, VIIRS and GOES.
    They also provide preprocessed datasets such as land cover, temperature, 
    wind direction, vegetation index (NDVI), MODIS active fire, etc.
    The API is free. A [sign up](https://earthengine.google.com/signup/) is required.
    Takes a couple of days for approval.
- [Sentinel Hub](https://www.sentinel-hub.com/)
    Provides APIs for Sentinel, Landsat and MODIS. 
    They also provide [EO Browser](https://apps.sentinel-hub.com/eo-browser/) 
    and [Sentinel Hub playground](https://apps.sentinel-hub.com/sentinel-playground/)
    to explore their API before subscribing. They offer a free trial of 30 days.
- [Copernicus](https://scihub.copernicus.eu/)
    Provides APIs for Sentinel products.
- [Earth Explorer](https://earthexplorer.usgs.gov/)
    Visualises satellite images. There isn't an official public API for bulk-downloading images.

Out of the above, we implemented downloading functionalities for both Google Earth Engine and Sentinel Hub. 
Below, we describe how you could use our download tools.

## Google Earth Engine

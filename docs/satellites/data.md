## Satellite Image Providers

There are many sources that host publicly available satellite images.
We list a few alternatives below:

- [Google Earth Engine](https://earthengine.google.com/)
    Hosts a wide collection of publicly available satellite imagery data, 
    including but not limited to Sentinel, Landsat, MODIS, VIIRS and GOES.
    They also provide preprocessed datasets such as land cover, temperature, 
    wind direction, vegetation index (NDVI), MODIS active fire, etc.
    The API is free. A [sign up](https://earthengine.google.com/signup/) is required.
    
    They have an amazing [interactive editor / visualiser](code.earthengine.google.com/).
    
    You may also want to register a service account to authenticate your backend. 
    This may take a couple of days for approval.
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
Below, we describe how you can use our download tools.

## Google Earth Engine
Google Earth Engine (GEE) is probably the best platform to use for projects involving satellite image analysis. 
They provide an [interactive coding environment](https://code.earthengine.google.com/) where you can filter and preprocess images, 
and see the visualisation results immediately overlaid on top of Google Maps.

You might want to spend a couple of days getting a good understanding of how GEE works.
An important thing to understand when writing filtering or pre-processing code for GEE is that, 
what the code returns is a computational graph, rather than the execution results of that operation.
The computational graph is executed in one go, only when the results are needed, 
such as when you request information via `.info()`, get a download link, or show the image on a map.

This is because all the preprocessing step is handled by Google's server. 
The amount of data stored on Google's server is massive, and if we were to download them onto our local machines, 
a lot of data needs to be transmitted. 
By creating a computational graph and passing that graph along with the data request,
Google can do all the computational steps for us and just provide us the final result, whether that be a value or a link to an image.

This makes it rather complicated to download image tiles compared to other APIs (e.g. Sentinel Hub).
However we have written some scripts that do this, which we hope would be helpful for your purpose as well.

Here are the steps required to start using Google Earth Engine API.

### 1. Sign up for the API
[Sign up](https://earthengine.google.com/signup/) to start using the API and the [interactive coding environment](https://code.earthengine.google.com/).

### 2. Register your service account to use GEE
By completing step 1 you can authenticate yourself to use the API. 
The problem is that, when you have a script you want to run, you don't want to be manually authenticating it every time.
Also, if you are developing a RESTful API, you need a way of not requiring the user to sign up for GEE but use your server-side credentials instead.
This is why registering a service account can be useful. The steps are described in the [service accounts documentation](https://developers.google.com/earth-engine/service_account).
There is a registration form that you need to fill out. The registration process may take a couple of days.

### 3. Download json key
Once you have registered your service account, you should be able to [create and download your service account key](https://console.developers.google.com/iam-admin/serviceaccounts/details/).
The JSON key file is called `privatekey.json` by default. If you want to use our code, rename your json key file to `gee_key.json` and place it under `resources/gee/`.
An example of a JSON key file can be found at `resources/gee/gee_key_example.json`.

### 4. Resources and Documentation
More resources can be found in the official documentation:
- [Google Earth Engine - Python Install](https://developers.google.com/earth-engine/python_install)

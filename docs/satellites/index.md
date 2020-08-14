# Satellite Imagery

## Satellite Image Providers

There are many sources that host publicly available satellite images.
We list a few alternatives below:

- **[Google Earth Engine](https://earthengine.google.com/)**
    
    Hosts a wide collection of publicly available satellite imagery data, 
    including but not limited to Sentinel, Landsat, MODIS, VIIRS and GOES.
    They also provide preprocessed datasets such as land cover, temperature, 
    wind direction, vegetation index (NDVI), MODIS active fire, etc.
    The API is free. A [sign up](https://earthengine.google.com/signup/) is required.
    
    They have an amazing [interactive editor / visualiser](code.earthengine.google.com/).
    
    You may also want to register a service account to authenticate your backend. 
    This may take a couple of days for approval.
- **[Sentinel Hub](https://www.sentinel-hub.com/)**
    
    Provides APIs for Sentinel, Landsat and MODIS. 
    They also provide [EO Browser](https://apps.sentinel-hub.com/eo-browser/) 
    and [Sentinel Hub playground](https://apps.sentinel-hub.com/sentinel-playground/)
    to explore their API before subscribing. They offer a free trial of 30 days.
- **[Copernicus](https://scihub.copernicus.eu/)**
    
    Provides APIs for Sentinel products.
    
- **[Earth Explorer](https://earthexplorer.usgs.gov/)**
    
    Visualises satellite images. There isn't an official public API for bulk-downloading images.

Out of the above, we implemented downloading functionalities for both Google Earth Engine and Sentinel Hub. 

## Google Earth Engine
Google Earth Engine (GEE) is probably the most comprehensive platform to use for projects involving satellite image analysis. 
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

Please refer to the [README.md in the repo](https://github.com/oxai/wildfire/tree/master/resources/gee/README.md)
to find out about the steps required to start using Google Earth Engine API and using our code.

## Sentinel Hub API
[Sentinel Hub](https://www.sentinel-hub.com/) is another API that can be useful for downloading sentinel, landsat and MODIS products.
Unlike Google Earth Engine, the free trial only lasts for 30 days, and the quota for the amount of download is tighter.
Compared to GEE, Sentinel Hub is easier to get started with since it focusses on a set of APIs that can meet most common use cases, 
whereas GEE gives you far more customisability in the preprocessing step, but also adds complexity to the process.

Please refer to the [README.md in the repo](https://github.com/oxai/wildfire/tree/master/resources/sentinelhub/README.md)
for set up instructions.

## Glossary

**Organizations**
- NASA (National Aeronautics and Space Admistration)
- NOAA (National Oceanic and Atmospheric Administration)
- USGS (U.S. Geological Survey)
- ESA (European Space Agency)
- JMA (Japan Meteorological Agency)
- GFW (Global Forest Watch)
- FIRMS (Fire Information for Resource Management System)

**Satellite Programmes**
- Landsat
- Sentinel
- NOAA

**Satellites**  
- Landsat 8 (USGS & NASA)
- Sentinel 2[A] (ESA)
- Sentinel 2[B] (ESA) (identical to Sentinel2A but with orbit shifted 180°)
- Terra (NASA)
- Aqua (NASA)
- Himawari-8 (JMA)
- NOAA-20 (NOAA)

Each satellite carries one or more instrumenets to detect electromagnetic
radition from the earth. The detected radiation is divided into bands of
different frequency (or wavelength) ranges. 


**Instruments**

| Instrument    | Satellite it's on | Bands and resolutions     | Life              |
| ----------    | ----------------- | ---------------------     | ----              |
| VIIRS         | NOAA-20           | 16@750m, 6@375m           | 11/2017-present   |
| MODIS         | Terra             | 2@250m, 5@500m, 29@1000m  | 12/1999-present   |
| OLI           | Landsat8          | 8@30m, 1@15m              | 02/2013-present   |
| ASTER	        | Terra	            | 4@15m, 6@30m, 5@90m	    | 12/1999-present   |
| CERES	        | Terra, Aqua	    | 13@1000m	                | 12/1999-present   |
| MISR	        | Terra	            | 4@250	                    | 12/1999-present   |
| MOPITT	    | Terra	            | 3@22000	                | 12/1999-present   |
| AMSR-E	    | Aqua	            | 4,8,18,16,29,43	        | 05/2002-present   |
| AMSU	        | Aqua	            | 15@45000, 5@15000	        | 05/2002-present   |
| AIRS	        | Aqua	            | 4@2300                    | 05/2002-present   |
| MSI           | Sentinel2         | 3@60m, 6@50m, 4@10m       | 06/2015-present   |
| AVHRR         | NOAA-19           | 5@1100m                   | 02/2009-present   |
| SLSTR	        | Sentinel3	        | 5@500m, 5@1000m	        | 02/2016-present   |
| OLCI	        | Sentinel3	        | 21@300m	                | 02/2016-present   |
| SRAL	        | Sentinel3	        | 300m	                    | 02/2016-present   |


**Instrument Acronyms**
- VIIRS (Visible Infrared Imaging Radiometer Suite) 375m
- MODIS (Moderate Resolution Imaging Spectroradiometer
- AVHRR (Advanced Very-High-Resolution Radiometer)
- ASTER (Advanced Spaceborne Thermal Emission and Reflection Radiometer)
- OLI (Operational Land Manager)
- MSI (Multi-Spectral Instrument)
- CERES (Clouds and the Earth's Radiant Energy System)
- MISR (Multi-angle Imaging SpectroRadiometer)
- MODIS (Moderate-resolution Imaging Spectroradiometer)[5]
- MOPITT (Measurements of Pollution in the Troposphere)[6]
- TIRS (Thermal Infrared Sensor)
- AMSR-E (Advanced Microwave Scanning Radiometer-EOS)
- AMSU (Advanced Microwave Sounding Unit)
- AIRS (Atmospheric Infrared Sounder)
- HSB (Humidity Sounder for Brazil)
- SLSTR (Sea and Land Surface Temperature Radiometer)
- OLCI (Ocean and Land Colour Instrument)
- SRAL (Synthetic Aperture Radar Altimeter)

---
Written by Louis Mahon, Shu Ishida
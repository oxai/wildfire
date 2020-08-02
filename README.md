# Wildfire Forecasting from Satellite Imagery
OxAI Labs Earth and Space Project

## Initial setup
#### Conda environment
We recommend installing `conda` to manage the python environment. 

`conda create --name <your-env-name> python=3.7`
`conda activate <your-env-name>`

#### Install Dependencies
`pip install -r requirements_minimum.txt`

## Set up Google Earth Engine
You need to [sign up to use Google Earth Engine](https://earthengine.google.com/signup/) in order to use this free API.
Please refer to the [README for Google Earth Engine](https://github.com/oxai/wildfire/blob/master/resources/gee/README.md)
for more details.

## Set up Sentinelhub
This is optional, and you may not require it if you are able to set up Google Earth Engine.
Please refer to the [README for Sentinel Hub](https://github.com/oxai/wildfire/blob/master/resources/sentinelhub/README.md)
for more details.

## Datasets
### FPA-FOD Dataset
Download [FPA_FOD_20170508.sqlite](https://www.kaggle.com/rtatman/188-million-us-wildfires) and place it in the ```resources/fpa_fod/data_dir/``` directory.

### MODIS fire archive
Follow the [instructions in the MODIS Fire directory](https://github.com/oxai/wildfire/blob/master/resources/modis_fire/README.md).

### GlobFire Dataset
Follow the [instructions in the GlobFire directory](https://github.com/oxai/wildfire/blob/master/resources/globfire/README.md).

## Models
The code in the `models` directory is at an experimental stage, and is not intended to be used at its current state.
We developed this code to test a simple CNN model to classify images that capture wildfire and those which don't.
While the result was promising, we were only able to demonstrate this for a small dataset with obvious wildfire images.

Please see here for more discussion on [the challenges of approaches that use machine learning for wildfire identification](https://oxai.github.io/wildfire/challenges/).

## Web app
There are [optional setup instructions](https://github.com/oxai/wildfire/tree/master/web/README.md) required only if you want to try out our Django webapp to visualise the map.

#### Errors
If you are encountering errors on Mac such as
```
Attempting to bind to HOST environment variable
```
[this medium article](https://medium.com/@choy/fixing-create-react-app-when-npm-fails-to-start-because-your-host-environment-variable-is-being-4c8a9fa0b461) might help you solve the problem. Set your `HOST` variable to `localhost` in bash.

You may encounter installation issues with GeoPandas on Windows. Try
`conda install -c conda-forge geopandas`
If that doesn't work, follow [this instruction for Windows](https://geoffboeing.com/2014/09/using-geopandas-windows/) 
and install GDAL, Fiona, pyproj, rtree, and shapely from [Gohlke (unofficial repository for Windows binaries)](https://www.lfd.uci.edu/~gohlke/pythonlibs/).

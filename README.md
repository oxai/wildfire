# Wildfire Forecasting from Satellite Imagery
OxAI Labs Earth and Space Project

## Initial setup
### Initial Setup Required for Web App with Google Earth Engine
The web app in `web` uses `Django` as its backend framework, and `React` as its frontend framework. 

#### Conda environment
We recommend installing `conda` to manage the python environment. 

`conda create --name <your-env-name> python=3.7`
`conda activate <your-env-name>`

#### Dependencies
`pip install 
django
earthengine-api
django-cors-headers
djangorestframework
numpy
pillow
matplotlib
scikit-image
geopandas
`

Alternatively, run
`pip install -r requirements_minimum.txt`

#### Install Node.js
The frontend React framework is developed in Node.js. Download and install the latest stable version from https://nodejs.org/en/download/.

#### Set up Google Earth Engine
Download `gee_key.json` from Google Drive and place it at `resources/gee/gee_key.json`, which contains Google Earth Engine server login credentials (do not commit to git!).

#### Set up Django
Download `app_key.json` from Google Drive and place it at `web/app_key.json`, which contains Django secret key (do not commit to git!).

### Running the web servers
In one terminal, run the following to start up the Django backend server:
```
cd web
python manage.py runserver
```

In another terminal, run the following to start up a development server for React frontend:

```
cd web/frontend
npm install   # just after updating your branch
npm start
```

Navigate to http://localhost:3000/

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
### Using Sentinelhub
Please refer to `/resources/sentinelhub/README.md`

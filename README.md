# Wildfire Forecasting from Satellite Imagery
OxAI Labs Earth and Space Project

## Initial setup
#### Conda environment
We recommend installing `conda` to manage the python environment. 

`conda create --name <your-env-name> python=3.7`
`conda activate <your-env-name>`

#### Install Dependencies
`pip install -r requirements_minimum.txt`

#### Set up Google Earth Engine
You need to [sign up to use Google Earth Engine](https://earthengine.google.com/signup/) in order to use this free API.
Please refer to the [README for Google Earth Engine](https://github.com/oxai/wildfire/blob/master/resources/gee/README.md)
for more details.

---

Below are optional setup required only if you want to try out our Django webapp to visualise the map.

---

### Initial Setup Required for Web App with Google Earth Engine
The web app in `web` uses `Django` as its backend framework, and `React` as its frontend framework. 

#### Install Node.js
The frontend React framework is developed in Node.js. Download and install the latest stable version from https://nodejs.org/en/download/.

#### Set up Django
Create a file called `app_key.json` at `web/app_key.json`, which contains Django secret key.
```
{
  "django_secret": "some-random-string"
}
```

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

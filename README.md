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
`

Alternatively, run
`pip install requirements_minimum.txt`

### Running the web servers
In one terminal, run the following to start up the Django backend server:
```
cd web
python manage.py runserver
```

In another terminal, run the following to start up a development server for React frontend:

```
cd web/frontend
npm install   # just for the first run
npm start
```

Navigate to http://localhost:3000/

### Using Sentinelhub
Please refer to `/resources/sentinelhub/README.md`

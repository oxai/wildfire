## Satellite image visualiser web app

### Initial Setup Required for Web App with Google Earth Engine
The web app uses `Django` as its backend framework, and `React` as its frontend framework. 

#### Install Node.js
The frontend React framework is developed in Node.js. Download and install the latest stable version from https://nodejs.org/en/download/.

#### Set up Django
Create a file called `app_key.json` in this directory, with a custom Django secret key.
```
{
  "django_secret": "some-random-string"
}
```

### Running the web servers
In one terminal, run the following to start up the Django backend server:
```
python manage.py runserver
```

In another terminal, run the following to start up a development server for React frontend:

```
cd frontend
npm install   # just after updating your branch
npm start
```

Navigate to http://localhost:3000/

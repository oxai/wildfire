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

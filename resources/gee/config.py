#!/usr/bin/env python
import ee, os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# The service account email address authorized by your Google contact.
# Set up a service account as described in the README.

# The private key associated with your service account in JSON format.
EE_PRIVATE_KEY_FILE = os.path.join(BASE_DIR, 'gee_key.json')

with open(EE_PRIVATE_KEY_FILE, 'r') as f:
    data=f.read()

key_json = json.loads(data)

EE_ACCOUNT = key_json['client_email']
EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)

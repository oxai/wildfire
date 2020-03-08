#!/usr/bin/env python
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EE_PRIVATE_KEY_FILE = os.path.join(BASE_DIR, 'app_key.json')

with open(EE_PRIVATE_KEY_FILE, 'r') as f:
    data=f.read()

key_json = json.loads(data)
DJANGO_SECRET = key_json["django_secret"]
